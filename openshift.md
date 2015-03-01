# Crane on Openshift

1. Set application environment variables. NOTE: This may work as openshift action_hooks in `.openshift/action_hooks/pre_build` where env vars may be exported.
```
$ sudo rhc env set OPENSHIFT_PYTHON_WSGI_APPLICATION=crane/wsgi.py --app <my_openshift_app> --namespace <my_openshift_domain>
Setting environment variable(s) ... done
$ sudo rhc env set OPENSHIFT_PYTHON_DOCUMENT_ROOT=crane/ --app <my_openshift_app> --namespace <my_openshift_domain>
Setting environment variable(s) ... done
```
1. FIXME: remove python-rhsm dependency
1. Edit configuration file
```
[general]
debug: false
data_dir: app-root/repo/crane/data
data_dir_polling_interval: 60
endpoint:

[gsa]
url:
```
1.Add metadata file(s) to data directory

```
$ cp centos.json crane/data/centos.json
```
1. Git add, commit, push to openshift to restart app
