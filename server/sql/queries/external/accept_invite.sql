-- Query to accept an external invite
-- Parameters:
--   %(invite_id)s - ID of the invite
SELECT accept_external_invite(%(invite_id)s) AS result;

