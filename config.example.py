AUTH_TOKEN = "TOKEN"

ALLOW_ADMIN_PROCESSES = True

process_names = ['notepad']

server_processes = {
    'notepad': {
        'dir': 'C:\\Windows',
        'exe': 'notepad.exe',
    },
}

acl_enabled = True
acl = {
    "user1": ["all"],
    "user2": ["status"],
}
