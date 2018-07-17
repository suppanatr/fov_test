from __future__ import print_function
from multiprocessing import Pool, current_process, cpu_count
import numpy as np
import time

def matmul(a,b):
    return a*b;

def diff_ang(a,b):
    r = a - b;
    if r > np.pi:
        r = r - 2 * np.pi;
    elif r < - np.pi:
        r = 2 * np.pi - r;
    return r;

def wraptopi(a):
    return (a + np.pi) % (2*np.pi) - np.pi;

'''
*********************
*********************
sim 2 with parameters
swarm agents attract to each other
*********************
*********************
'''
def start_AP(args):
    (ft,sRad,cRad,No) = args;

    #set file pointer
    fXname = 'sim1_time_' + str(ft) + '_' + str(sRad) + '_' + str(cRad) + '_' + str(No) +'_X.txt';
    fYname = 'sim1_time_' + str(ft) + '_' + str(sRad) + '_' + str(cRad) + '_' + str(No) +'_Y.txt';
    fEname = 'sim1_time_' + str(ft) + '_' + str(sRad) + '_' + str(cRad) + '_' + str(No) +'_E.txt';
    fWriteX = open(fXname,"w");
    fWriteY = open(fYname,"w");
    fWriteE = open(fEname,"w");
    #ar_arg = ft

    #set world
    #ft = 500
    final_time = ft; #total simulation time in sec
    ts = 0.1;    #time step length in sec
    total_ts = int(final_time / ts); #total step used in simulation

    sa_number = 50; #number of swarm agents
    ca_number = 1; #number of control agents
    total_agent = sa_number + ca_number; #number of agents

    #set swarm agent's parameters
    sa_speed = 1; #speed in unit/sec
    sa_turnRate = np.deg2rad(45); #turn rate in deg/sec
    sa_repRad = sRad; #repulsion radius in unit
    sa_attRad = 30;
    sa_oriRad = sa_repRad + 2;
    sa_ors = sa_oriRad * sa_oriRad;

    sa_fov = np.deg2rad(360 / 2);

    sa_fErrRatio = 0.1;
    sa_tErrRatio = 0.1;

    sa_fStep = sa_speed * ts; #forward step length in unit
    sa_tStep = sa_turnRate * ts; #turn step in rad
    sa_rrs = sa_repRad * sa_repRad; #square of repulsion radius
    sa_ars = sa_attRad * sa_attRad;

    sa_fErrSd = sa_fStep * sa_fErrRatio / 2;
    sa_tErrSd = sa_tStep * sa_tErrRatio / 2;


    #set control agent's parameters
    ca_speed = 1; #speed in unit/sec
    ca_turnRate = np.deg2rad(45); #turn rate in deg/sec
    ca_repRad = cRad; #repulsion radius in unit
    ca_attRad = 7; #attraction radians in unit

    ca_fErrRatio = 0.1;
    ca_tErrRatio = 0.1;

    ca_fStep = ca_speed * ts; #forward step length in unit
    ca_tStep = ca_turnRate * ts; #turn step in rad
    ca_rrs = ca_repRad * ca_repRad; #square of repulsion radius
    ca_ars = ca_attRad * ca_attRad;

    ca_fErrSd = ca_fStep * ca_fErrRatio / 2;
    ca_tErrSd = ca_tStep * ca_tErrRatio / 2;

    #initialise agents
    position = (np.random.rand(total_agent,2) - 0.5) * np.sqrt(sa_number);
    position_tmp = np.zeros((total_agent,2));

    direction = (np.random.rand(total_agent,1) * 2 * np.pi - np.pi);
    direction_tmp = np.zeros((total_agent,1));
    d_direction = direction;

    if ca_number > 0:
        #initialise control agent position
        position[sa_number,0] = np.sqrt(sa_number);
        position[sa_number,1] = np.sqrt(sa_number);
        direction[sa_number] = np.deg2rad(-135);
        d_direction[sa_number] = np.deg2rad(-135);
        pass


    if sa_number == 2:
        position[0,0] = -2;
        position[0,1] = 0;
        position[1,0] = 2;
        position[1,1] = 1;
        direction[0] = 0;
        direction[1] = np.pi;

    #preparing matrix
    #diff_xy_t = np.zeros((total_agent,2))
    expand_matrix = np.ones((total_agent,1))
    double_matrix = np.ones((1,2))
    #aad_t = np.zeros((total_agent,1))
    #start loop
    for t in range(total_ts):
        encounter175 = 0;
        encounter125 = 0;
        encounter150 = 0;
        nn_dist = 0;
        force = 0;
        #compute each swarm agent by rules
        for i in range(sa_number):
            #
            #sense others' distance
            diff_xy = matmul(expand_matrix,position[i,:]) - position
            dist_i = (np.square(diff_xy[:,0]) + np.square(diff_xy[:,1])).reshape(total_agent,1)
            dist_i[i,0] = 1
            
            aad = np.abs(wraptopi(np.arctan2(diff_xy[:,1],diff_xy[:,0]).reshape(total_agent,1) - direction))

            #check if in range
            in_rr = dist_i < (expand_matrix * sa_rrs);
            
            in_or = dist_i <= (expand_matrix * sa_ors);
            
            in_ar = (in_or != 1) * (dist_i <= (expand_matrix * sa_ars));
            
            in_or = (in_rr != 1) * (in_or);
            
            in_fov = aad < (expand_matrix * sa_fov)
            in_fov[i,0] = False
            
            in_rr = in_rr * in_fov;
            in_ar = in_ar * in_fov;
            in_or = in_or * in_fov;
            
            #print(i)
            desired_dir = d_direction[i];

            if(t%1 == 0): # check if time step is 0.5 sec
                if(in_rr.sum() > 0):
                    #compute desired direction with repulsion rule
                    sum_vect = ((diff_xy / matmul(dist_i, double_matrix)) * in_rr).sum(0);
                    desired_dir = np.arctan2(sum_vect[1],sum_vect[0]);
                    if sa_number == 2:
                        print("detected",i,np.rad2deg(desired_dir));
                else:
                    #compute desired direction with attraction rule
                    sum_vect_x = 0;
                    sum_vect_y = 0;
                    sum_vect_att = -((diff_xy) * in_ar).sum(0);
                    sum_vect_att_mag = np.sqrt(sum_vect_att[0]*sum_vect_att[0]+sum_vect_att[1]*sum_vect_att[1]);
                    sum_vect_ori_x = (np.cos(direction) * in_or).sum(0);
                    sum_vect_ori_y = (np.sin(direction) * in_or).sum(0);
                    sum_vect_ori_mag = np.sqrt(sum_vect_ori_x*sum_vect_ori_x+sum_vect_ori_y*sum_vect_ori_y);
                    if(in_ar.sum() > 0):
                        sum_vect_x += sum_vect_att[0]/sum_vect_att_mag;
                        sum_vect_y += sum_vect_att[1]/sum_vect_att_mag;
                    if(in_or.sum() > 0):
                        sum_vect_x += sum_vect_ori_x/sum_vect_ori_mag;
                        sum_vect_y += sum_vect_ori_y/sum_vect_ori_mag;
                    desired_dir = np.arctan2(sum_vect_y,sum_vect_x);
                    if sa_number == 2:
                        print(i,np.rad2deg(desired_dir));
                    if sa_number == 2:
                        print(i,np.rad2deg(desired_dir));


            #turn
            d_direction[i] = desired_dir;
            turning_angle = diff_ang(desired_dir,direction[i]);
            if sa_number == 2:
                print(np.rad2deg(turning_angle));
            # is turn rate enough
            if np.abs(turning_angle) <= sa_tStep:
                direction_tmp[i] = wraptopi(direction[i] + turning_angle + np.random.normal(0,sa_tErrSd,1)); # with error
                d_direction[i] = direction_tmp[i];
            else:
                direction_tmp[i] = wraptopi(direction[i] + sa_tStep * turning_angle / np.abs(turning_angle) + np.random.normal(0,sa_tErrSd,1));

            #move

            total_step_length = sa_fStep + np.random.normal(0,sa_fErrSd,1)
            position_tmp[i,0] = position[i,0] + np.cos(direction_tmp[i]) * total_step_length;
            position_tmp[i,1] = position[i,1] + np.sin(direction_tmp[i]) * total_step_length;

            if sa_number == 2:
                print(np.rad2deg(direction[i]),position[i,:]);
                print(np.rad2deg(direction_tmp[i]),position_tmp[i,:]);
                #raw_input();

        #compute each control agent by rules
        for i in range(sa_number,total_agent):
            #print(i)
            #sense others' distance
            diff_xy = matmul(expand_matrix,position[i,:]) - position
            dist_i = (np.square(diff_xy[:,0]) + np.square(diff_xy[:,1])).reshape(total_agent,1)
            dist_i[i,0] = 1
            #dist_i = np.delete(dist_i,i,0);
            #check if in range
            in_rr = dist_i < expand_matrix * ca_rrs;
            in_rr_150 = dist_i < expand_matrix * ca_rrs * 1.5;
            in_rr_125 = dist_i < expand_matrix * ca_rrs * 1.25;
            in_rr_175 = dist_i < expand_matrix * ca_rrs * 1.75;
            in_ar = (in_rr != 1) * (dist_i <= expand_matrix * ca_ars);
            
            in_rr[i,0] = False
            in_ar[i,0] = False
            
            encounter175 = in_rr_175.sum();
            encounter125 = in_rr_125.sum();
            encounter150 = in_rr_150.sum();
            nn_dist = np.sqrt(dist_i.min());
            desired_dir = d_direction[i];

            #compute sumvect
            sum_vect = -((diff_xy) * in_ar).sum(0);
            force = np.sqrt(np.square(sum_vect[1])+np.square(sum_vect[0]));

            if(t%1 == 0): # check if time step is 0.5 sec
                if(in_rr.sum() > 0):
                    #compute desired direction with repulsion rule
                    sum_vect = ((diff_xy / matmul(dist_i, np.ones((1,2)))) * in_rr).sum(0);
                    desired_dir = np.arctan2(sum_vect[1],sum_vect[0]);
                    if sa_number == 2:
                        print("detected",i,np.rad2deg(desired_dir));
                elif(in_ar.sum() > 0):
                    #compute desired direction with attraction rule
                     #put sumvect out of condition -> always compute
                    sum_vect = -((diff_xy) * in_ar).sum(0);
                    desired_dir = np.arctan2(sum_vect[1],sum_vect[0]);
                    #sum_vect = -((diff_xy / matmul(dist_i, np.ones((1,2)))) * in_ar).sum(0);

            #turn
            d_direction[i] = desired_dir;
            turning_angle = diff_ang(desired_dir,direction[i]);
            if sa_number == 2: #for debug
                print(np.rad2deg(turning_angle));
            # is turn rate enough
            if np.abs(turning_angle) <= ca_tStep:
                direction_tmp[i] = wraptopi(direction[i] + turning_angle + np.random.normal(0,ca_tErrSd,1)); # with error
                d_direction[i] = direction_tmp[i];
            else:
                direction_tmp[i] = wraptopi(direction[i] + ca_tStep * turning_angle / np.abs(turning_angle) + np.random.normal(0,ca_tErrSd,1));
            #print(t,desired_dir,)

            #move
            total_step_length = ca_fStep + np.random.normal(0,ca_fErrSd,1)
            position_tmp[i,0] = position[i,0] + np.cos(direction_tmp[i]) * total_step_length;
            position_tmp[i,1] = position[i,1] + np.sin(direction_tmp[i]) * total_step_length;



        #store something?
        for tmp in position[:,0]:
            print("%.2f " % (tmp),file = fWriteX,end="");
        print("",file = fWriteX,end="\n");
        for tmp in position[:,1]:
            print("%.2f " % (tmp),file = fWriteY,end="");
        print("",file = fWriteY,end="\n");
        print("%d %d %d %.2f %.2f" % (encounter125,encounter150,encounter175,nn_dist,force),file = fWriteE,end="\n");

        #update state
        direction = np.copy(direction_tmp);
        position = np.copy(position_tmp);

    #post process?

    fWriteX.close();
    fWriteY.close();
    fWriteE.close();


def create_arg():
    finaltime = [500]
    #sa_rad = 10+np.arange(-2,3,1);
    sa_rad = [10];
    No = range(1,11)

    a=[]
    b=[]
    c=[]
    d=[]

    for ft in finaltime:
        for sr in sa_rad:
            #ca_rad = sr + np.arange(-2,3,1);
            ca_rad = [sr]
            for cr in ca_rad:
                for no in No:
                    a.append(ft);
                    b.append(sr);
                    c.append(cr);
                    d.append(no);

    return zip(a,b,c,d)

if __name__ == "__main__":
    #start_AP((500,10,10,1))

    pool = Pool(processes=1)
    arg = create_arg();

    now = time.time();
    pool.map( start_AP, arg )
    print(time.time() - now);
