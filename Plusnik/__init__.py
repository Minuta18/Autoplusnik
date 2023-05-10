# Autoplusnik Copyright (C) 2023 Igor Samsonov

from .update import update
from .readToken import readStepikToken, readGoogleToken
from .updateManager import add_task, run, UpdateQueue, UpdateTask
from threading import Thread

update_thread = Thread(target=run, args=())
update_thread.start()