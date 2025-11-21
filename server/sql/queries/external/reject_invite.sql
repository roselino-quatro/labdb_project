-- Query to reject an external invite
-- Parameters:
--   %(invite_id)s - ID of the invite
SELECT reject_external_invite(%(invite_id)s) AS result;

