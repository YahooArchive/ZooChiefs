Zookeeper Distributed Process Chiefs
=============

Goal
----

To be able to reliably use zookeeper to control the invocation of a distributed
systems applications, allowing there to be 1 'primary' process leader with X
backup process leaders (who will become active if the first primary leader either
exits successfully or exists incorrectly).

1. Uses zookeeper leader election to attempt to guarantee who is the currently
   active single process (with-in the limits of zookeeper).
1. Make programs which are potentially unsafe to run simultaneous instances of
   have the capability to have fail-over instances which will automatically get
   turned on.

Install
-------

    sudo pip-python install -r tools/pip-requires
    sudo python setup.py install

Get a zookeeper server up and running.

* http://zookeeper.apache.org/doc/current/zookeeperStarted.html

Example
-------

    # Start zookeeper
    $ZOOKEEPER_DIR/bin/zkServer.sh start
    
    # On one terminal
    solo.py -v  `which python` tools/spinner.py
    
    # On a second terminal
    solo.py -v  `which python` tools/spinner.py
