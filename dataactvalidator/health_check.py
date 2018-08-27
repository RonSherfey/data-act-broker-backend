import logging
from flask import Flask
from dataactcore.config import CONFIG_SERVICES
from dataactcore.logging import configure_logging
from dataactcore.utils.jsonResponse import JsonResponse

    """Datadog import"""
USE_DATADOG = False

if USE_DATADOG:
    import blinker as _
    from flask import Flask
    from ddtrace import tracer
    from ddtrace.contrib.flask import TraceMiddleware


logger = logging.getLogger(__name__)


def create_app():
    """Create the Flask app."""
    flask_app = Flask(__name__.split('.')[0])
    flask_app.debug = CONFIG_SERVICES['debug']
    flask_app.config.from_object(__name__)

    @flask_app.route("/", methods=["GET"])
    def test_app():
        """Confirm server running."""
        return "Validator is running"

    JsonResponse.debugMode = flask_app.debug

    return flask_app


def run_app():
    """Run the application."""
    flask_app = create_app()

    """This is for DataDog"""
    if USE_DATADOG:
        traced_app = TraceMiddleware(flask_app, tracer, service="broker", distributed_tracing=False)
        
    flask_app.run(
        threaded=True,
        host=CONFIG_SERVICES['validator_host'],
        port=CONFIG_SERVICES['validator_port']
    )
if __name__ == "__main__":
    configure_logging()
    run_app()
