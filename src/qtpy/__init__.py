import sys

import picologging
from picologging import DEBUG, Logger, getLogger
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine

from .environments import DesktopEnvironment, IEnvironment
from .project import PythonProject


class DesktopApplication(QGuiApplication):
    """Desktop application."""

    def __init__(self, args: list[str], environment: IEnvironment) -> None:
        """Initialize the application."""
        super().__init__(args)
        # Initialize the environment.
        self.__environment = environment

        # Initialize the default logger.
        picologging.basicConfig(level=DEBUG, format="%(levelname)s: %(message)s")
        self.__logger = getLogger(DesktopApplication.__name__)

        if ("--reload" in args) or ("-r" in args):
            self.logger.info("Enable hot reload")

        icon_path = self.environment.content_root_path / self.environment.assets_path / "logo.jpg"
        icon = QIcon(str(icon_path))
        self.setWindowIcon(icon)

        # Load the main qml file.
        qml_path = self.environment.content_root_path / "src" / "App.qml"
        self.__qml_engine = QQmlApplicationEngine()
        self.__qml_engine.load(qml_path)

    @property
    def configuration(self) -> object:
        raise NotImplementedError()

    @property
    def environment(self) -> IEnvironment:
        """Get the environment."""
        return self.__environment

    @property
    def lifetime(self) -> object:
        raise NotImplementedError()

    @property
    def logger(self) -> Logger:
        """Get the logger."""
        return self.__logger

    @property
    def services(self) -> object:
        raise NotImplementedError()

    @classmethod
    def create_builder(
        cls,
        args: list[str],
        app_name: str = "",
        content_root_path: str = "",
        asserts_path: str = "",
        environment: str = "",
    ) -> "DesktopApplicationBuilder":
        """Create a builder for the application."""
        return DesktopApplicationBuilder(args, app_name, content_root_path, asserts_path, environment)

    def run(self) -> None:
        """Run the application."""
        if not self.__qml_engine.rootObjects():
            self.logger.error("Application failed to load.")
            sys.exit(-1)

        self.logger.info("Application started.")
        self.logger.info(f"Environment: {self.environment}")
        self.logger.info(f"Content root path: {self.environment.content_root_path}")

        sys.exit(self.exec())


class DesktopApplicationBuilder:
    """Desktop application builder."""

    def __init__(
        self,
        args: list[str],
        app_name: str,
        content_root_path: str = "",
        assets_path: str = "",
        environment_name: str = "",
    ) -> None:
        """Initialize the builder."""
        self.__args = args
        self.__app_name = app_name
        self.__environment = DesktopEnvironment(environment_name, content_root_path, assets_path)

    @property
    def configuration(self) -> object:
        raise NotImplementedError()

    @property
    def environment(self) -> IEnvironment:
        """Get the environment."""
        return self.__environment

    @property
    def host(self) -> object:
        raise NotImplementedError()

    @property
    def logging(self) -> object:
        raise NotImplementedError()

    @property
    def services(self) -> object:
        raise NotImplementedError()

    @property
    def web_host(self) -> object:
        raise NotImplementedError()

    def build(self) -> DesktopApplication:
        """Build the application."""
        app_name = self.__app_name or PythonProject.name()
        version = PythonProject.version()

        QGuiApplication.setOrganizationName("Richill Capital")
        QGuiApplication.setOrganizationDomain("richillcapital.com")
        QGuiApplication.setApplicationName(f"ApplicationName = {app_name} - {version}")
        QGuiApplication.setApplicationDisplayName(f"ApplicationDisplayName = {app_name} - {version}")
        QGuiApplication.setApplicationVersion(version)

        app = DesktopApplication(self.__args, self.environment)

        return app


__all__ = ["DesktopApplication", "DesktopApplicationBuilder"]
