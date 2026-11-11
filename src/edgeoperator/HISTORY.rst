Release History
===============

1.0.0b4
++++++++
* Add the ``aldo log-collection collect``, ``collect-indirect``, ``show``, ``list``, and ``wait`` commands.
* Log collection commands wait for completion and return the created job by default.
* Add ``--no-wait`` to return ``status: Accepted`` and an ``operationStatusUrl`` for checking progress later.
* Add ``wait --operation-status-url`` to resume waiting and return the completed log collection.
* Add the ``aldo billing-configuration show`` and ``create`` commands, and the ``aldo billing-configuration snapshot show``
  and ``list`` commands.

1.0.0b3
++++++++
* Add the ``aldo system-configuration show`` and ``aldo system-configuration create`` commands.

1.0.0b2
++++++++
* Add the ``aldo observability-configuration show`` command.

1.0.0b1
++++++++
* Initial preview release with the system readiness show command.
