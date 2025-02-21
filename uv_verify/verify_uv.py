import subprocess
import sys
import os
import platform
from pathlib import Path
import logging
import json


class UVVerifier:
    def __init__(self):
        # Setup logging
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger("UVVerifier")

    def check_uv_installation(self):
        """Verify UV is installed and get version"""
        try:
            result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                self.logger.info(f"UV is installed: {result.stdout.strip()}")
                return True
            return False
        except FileNotFoundError:
            self.logger.error("UV is not installed or not in PATH")
            return False

    def verify_venv_creation(self):
        """Test virtual environment creation"""
        test_venv_path = Path("test_venv")
        try:
            # Create test venv
            subprocess.run(["uv", "venv", str(test_venv_path)], check=True)

            # Verify venv structure
            required_files = [
                test_venv_path
                / ("Scripts" if platform.system() == "Windows" else "bin"),
                test_venv_path / "lib",
                test_venv_path
                / (
                    "pyvenv.cfg"
                    if platform.system() != "Windows"
                    else "Scripts/activate"
                ),
            ]

            all_exist = all(path.exists() for path in required_files)

            if all_exist:
                self.logger.info("Virtual environment creation: SUCCESS")
            else:
                self.logger.error("Virtual environment missing required files")

            # Cleanup
            if test_venv_path.exists():
                import shutil

                shutil.rmtree(test_venv_path)

            return all_exist
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to create virtual environment: {e}")
            return False

    def test_package_installation(self):
        """Test package installation capabilities"""
        test_venv_path = Path("test_venv")
        try:
            # Create test venv
            subprocess.run(["uv", "venv", str(test_venv_path)], check=True)

            # Activate venv and install a simple package
            activate_script = (
                test_venv_path
                / ("Scripts" if platform.system() == "Windows" else "bin")
                / ("activate.bat" if platform.system() == "Windows" else "activate")
            )

            install_cmd = (
                f"source {activate_script} && uv pip install requests"
                if platform.system() != "Windows"
                else f"call {activate_script} && uv pip install requests"
            )

            result = subprocess.run(install_cmd, shell=True, check=True)

            if result.returncode == 0:
                self.logger.info("Package installation test: SUCCESS")
                success = True
            else:
                self.logger.error("Package installation failed")
                success = False

            # Cleanup
            if test_venv_path.exists():
                import shutil

                shutil.rmtree(test_venv_path)

            return success
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Package installation test failed: {e}")
            return False

    def check_cache_functionality(self):
        """Verify UV cache operations"""
        try:
            # Check cache directory
            cache_dir_result = subprocess.run(
                ["uv", "cache", "dir"], capture_output=True, text=True
            )
            if cache_dir_result.returncode != 0:
                self.logger.error("Failed to get cache directory")
                return False

            cache_dir = cache_dir_result.stdout.strip()
            self.logger.info(f"Cache directory: {cache_dir}")

            # Test cache clear
            clear_result = subprocess.run(
                ["uv", "cache", "clear"], capture_output=True, text=True
            )
            if clear_result.returncode != 0:
                self.logger.error("Failed to clear cache")
                return False

            self.logger.info("Cache functionality: SUCCESS")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Cache functionality test failed: {e}")
            return False

    def verify_pip_compatibility(self):
        """Verify UV's pip compatibility"""
        try:
            # Test pip list functionality
            result = subprocess.run(
                ["uv", "pip", "list"], capture_output=True, text=True
            )
            if result.returncode != 0:
                self.logger.error("Failed to run 'uv pip list'")
                return False

            self.logger.info("Pip compatibility: SUCCESS")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Pip compatibility test failed: {e}")
            return False

    def run_all_checks(self):
        """Run all verification checks and return results"""
        results = {
            "uv_installed": self.check_uv_installation(),
            "venv_creation": self.verify_venv_creation(),
            "package_installation": self.test_package_installation(),
            "cache_functionality": self.check_cache_functionality(),
            "pip_compatibility": self.verify_pip_compatibility(),
        }

        # Print summary
        self.logger.info("\n=== UV Installation Verification Summary ===")
        for check, result in results.items():
            status = "✓ PASS" if result else "✗ FAIL"
            self.logger.info(f"{check}: {status}")

        return results


if __name__ == "__main__":
    verifier = UVVerifier()
    results = verifier.run_all_checks()

    # Exit with appropriate status code
    sys.exit(0 if all(results.values()) else 1)
