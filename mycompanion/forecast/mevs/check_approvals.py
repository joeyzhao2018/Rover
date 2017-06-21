import json
import subprocess as sub

def check_mev_approval(db):
    #mev_approvals = json.load(open('/root/mev_approval.json', 'r'))
    mev_approvals = db.fetch_mevs()
    print('approvals: {}'.format(mev_approvals))
    unapproved_l = []
    for mev in mev_approvals:
        if not mev[3]:
            unapproved_l.append(mev)
    print("Unapproved MEVs: {}".format(unapproved_l))
    return unapproved_l

def send_reminder(approval_l):
    for approval in approval_l:
        print("Sending reminder for: {}".format(approval))
        print('Requesting approval for {} from {}'.format(approval[1], approval[2]))
        sub.call(['/home/pi/Documents/pyspace/email/sendMevApprovalNotification.sh', approval[1], approval[2]])
        
