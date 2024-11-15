import json
import sys

from ppg_runtime.application_context import cached_property
from ppg_runtime.application_context.PySide6 import ApplicationContext
from windows.window import MainWindow


class AppContext(ApplicationContext):
    def run(self):
        w = self.main_window
        a = self.app
        args = a.arguments()
        if len(args) > 1:
            input_path = args[-1]
            with open(
                input_path,
                "r",
            ) as input_file:
                jsdata = json.load(input_file)
            w.load_project_file(jsdata)

        w.show()
        return a.exec()

    @cached_property
    def app(self):
        """
        Overrides the default app function to pass in sys.argv to the
        QApplication object allowing to show the name of the app in
        titlebars such as MacOS and Linux
        """
        result = self._qt_binding.QApplication(sys.argv)
        result.setApplicationName(self.build_settings["app_name"])
        result.setOrganizationName(self.build_settings["app_name"])
        result.setApplicationVersion(self.build_settings["version"])
        return result

    @cached_property
    def main_window(self):
        return MainWindow()


if __name__ == "__main__":
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
