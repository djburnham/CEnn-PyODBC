-- Active transactions query 
SELECT sess_trans.session_id, open_transaction_count, sqltext.text
FROM sys.dm_tran_session_transactions sess_trans
INNER JOIN sys.dm_exec_connections cnxs
ON cnxs.session_id  = sess_trans.session_id
CROSS APPLY sys.dm_exec_sql_text(cnxs.most_recent_sql_handle) sqltext

--

SELECT  locks.request_session_id,locks.resource_type, request_mode, count(*) lockCount
FROM 
sys.dm_tran_locks locks
INNER JOIN 
sys.dm_tran_session_transactions sess_trans
ON 
sess_trans.session_id = locks.request_session_id
INNER JOIN 
sys.dm_exec_connections cnxs
ON 
cnxs.session_id = sess_trans.session_id
CROSS APPLY sys.dm_exec_sql_text(cnxs.most_recent_sql_handle) sqltext
GROUP BY request_session_id, resource_type, request_mode
