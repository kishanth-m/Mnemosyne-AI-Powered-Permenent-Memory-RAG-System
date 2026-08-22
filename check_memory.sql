-- check data

SELECT DISTINCT thread_id
FROM checkpoints;
SELECT *
FROM checkpoints;


-- delete query

TRUNCATE TABLE checkpoints, checkpoint_blobs, checkpoint_writes;