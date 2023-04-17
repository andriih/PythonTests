API_HOSTS = {
    "test": "http://192.168.0.9/wordpress/wp-json/wc/v3/",
    "dev": "",
    "prod": ""
}

WOO_API_HOSTS = {
    "test": "http://192.168.0.9/wordpress",
    "dev": "",
    "prod": ""
}

DB_HOST = {
    'machine1': {
        "test": {"host": "localhost",
                 "database": "quicksitedb",
                 "table_prefix": "wp_",
                 "socket": None,
                 "port": 3306
                 },
        "dev": {
            "host": "host.docker.internal",
            "database": "local",
            "table_prefix": "wp_",
            "socket": None,
            "port": 3306
        },
        "prod": {
            "host": "host.docker.internal",
            "database": "local",
            "table_prefix": "wp_",
            "socket": None,
            "port": 3306
        },
    },
    'docker': {
        "test": {
            "host": "host.docker.internal",
            "database": "wp398",
            "table_prefix": "wp2p_",
            "socket": None,
            "port": 3306
        },
        "dev": {
            "host": "host.docker.internal",
            "database": "local",
            "table_prefix": "wp_",
            "socket": None,
            "port": 3306
        },
        "prod": {
            "host": "host.docker.internal",
            "database": "local",
            "table_prefix": "wp_",
            "socket": None,
            "port": 3306
        },
    }
}
