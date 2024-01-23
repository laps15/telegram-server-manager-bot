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
    "user3": ["all", "~stop_server"],
    "user2": ["status"],
}
