from web import app
from web.worker import cleanup, resume_session


resume_session()

app.run(host='0.0.0.0', port=6080, threaded=True, debug=True, use_reloader=False)

cleanup()

