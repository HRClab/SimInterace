import MarkovDecisionProcess as MDP
import Controller as ctrl
import numpy as np
import matplotlib.pyplot as plt

#### Define the System ######

class doubleIntegrator(MDP.LinearQuadraticSystem):
    """
    Basic Newton's Laws
    """
    def __init__(self):
        dt = 0.1
        self.dt = dt
        self.x0 = np.array([1.0,0.0])
        A = np.eye(2) + dt * np.array([[0,1],[0,0]])
        B = dt * np.array([0,1])
        Q = dt * np.eye(2)
        R = dt * 1.
        dynMat = MDP.buildDynamicsMatrix(A,B)
        costMat = MDP.buildCostMatrix(Cxx=Q,Cuu=R)
        MDP.LinearQuadraticSystem.__init__(self,
                                           dynamicsMatrix=dynMat,
                                           costMatrix=costMat)

sys = doubleIntegrator()

#### Make a List of Controllers #####

T = 100
Controllers = []

staticCtrl = ctrl.staticGain(gain=-np.ones(2),Horizon=T,label='Static')
Controllers.append(staticCtrl)

lqrCtrl = ctrl.linearQuadraticRegulator(SYS=sys,Horizon=T,label='LQR')
Controllers.append(lqrCtrl)

mpcCtrl = ctrl.modelPredictiveControl(SYS=sys,
                                      predictiveHorizon=10,
                                      Horizon=T,
                                      label='MPC')
Controllers.append(mpcCtrl)

samplingCtrl = ctrl.samplingControl(SYS=sys,Horizon=T,
                                    KLWeight=1e-0,burnIn=100,
                                    ExplorationCovariance = 10.,
                                    label='Sampling')
Controllers.append(samplingCtrl)


#### Prepare the simulations ####
NumControllers = len(Controllers)
X = np.zeros((NumControllers,T+1,2))
Cost = np.zeros(NumControllers)
Time = sys.dt * np.arange(T+1)
plt.figure(1)
plt.clf()
line = []

print '\nComparing Controllers\n'

#### Simulate all of the controllers ####

for k in range(NumControllers):
    controller = Controllers[k]
    name = controller.label
    X[k], Cost[k] = sys.simulatePolicy(controller)
    print '%s: %g' % (name,Cost[k])
    handle = plt.plot(Time,X[k][:,0],label=name)[0]
    line.append(handle)

plt.legend(handles=line)
