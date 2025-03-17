If you suspect recent deadlocks, check system views:


SELECT *
FROM sys.dm_exec_requests
WHERE blocking_session_id <> 0;

o check the most recent deadlock event, use:

SELECT XEvent.query('(event/data/value)[1]') AS DeadlockGraph
FROM 
(
    SELECT CAST(target_data AS XML) AS TargetData
    FROM sys.dm_xe_session_targets AS st
    JOIN sys.dm_xe_sessions AS s 
    ON s.address = st.event_session_address
    WHERE s.name = 'system_health' 
    AND st.target_name = 'ring_buffer'
) AS SubQuery
CROSS APPLY TargetData.nodes('//RingBufferTarget/event') AS XEventData(XEvent)
WHERE XEvent.value('@name', 'varchar(4000)') = 'xml_deadlock_report';

SPID that is blocking other

SELECT blocking_session_id, session_id, wait_type, wait_time, wait_resource, status
FROM sys.dm_exec_requests
WHERE blocking_session_id <> 0;


FIND Query that is blocking

SELECT r.session_id, r.blocking_session_id, r.wait_type, r.wait_time, r.wait_resource,
       t.text AS BlockingQuery
FROM sys.dm_exec_requests r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE r.session_id = <BLOCKING_SESSION_ID>;  -- Replace with blocking_session_id


Find blocking ID details

SELECT session_id, blocking_session_id, status, wait_type, last_wait_type, wait_time, wait_resource
FROM sys.dm_exec_requests
WHERE session_id = <BLOCKING_SESSION_ID>;  -- Replace with blocking_session_id

OR 
SELECT s.session_id, s.host_name, s.program_name, s.login_name, s.status, r.wait_type
FROM sys.dm_exec_sessions s
LEFT JOIN sys.dm_exec_requests r ON s.session_id = r.session_id
WHERE s.session_id = <BLOCKING_SESSION_ID>;

KILL blocking

KILL <BLOCKING_SESSION_ID>;


Long running queries
SELECT 
    r.session_id, 
    r.start_time, 
    s.login_name, 
    r.status, 
    r.cpu_time, 
    r.total_elapsed_time / 1000 AS elapsed_time_sec,
    r.blocking_session_id,
    t.text AS running_query
FROM sys.dm_exec_requests r
JOIN sys.dm_exec_sessions s ON r.session_id = s.session_id
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE s.login_name = 'DOMAIN\ServiceAccount'  -- Change this to the actual service account
ORDER BY r.total_elapsed_time DESC;  -- Show longest-running first

Kill long running queries
KILL <SESSION_ID>;  -- Replace with actual session_id
