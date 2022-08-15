# How to deploy on VPS

1. Install docker
2. Navigate to project root folder
3. Run `docker compose up`
4. If there is error `Unknown MySQL server host 'db'`, run `docker compose up` one more time and everything will be OK. This error caused by fact that `depends_on` just wait when container will be upped byn not wait until it will be execute all initialization
