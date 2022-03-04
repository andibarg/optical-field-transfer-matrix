import numpy as np
import matplotlib.pyplot as plt

'''
Transfer matrix method

Inputs
wvl: wavelength
fulln: array with all refractive indices
fullw: array with all layer widths

Outputs:
r: reflection coefficient
t: transmission coefficient
x: position
Nn: refractive indices (vs x)
E: optical field (vs x)
'''
def tmm(wvl, fulln, fullw):
    # Exponent factors
    d = fullw*2*np.pi/wvl*fulln

    # Initiate arrays
    x = []
    E = []
    Nn = []
    N = len(fulln)
    M = np.zeros((2,2,N-1),dtype=complex)
    rs = np.zeros(N-1)
    ts = np.zeros(N-1)

    # Loop through layers
    for ii in range(N-1):

        # n of adjacent layers
        n1 = fulln[ii]
        n2 = fulln[ii+1]

        # Fresnel relations
        rs[ii] = (n1 - n2)/(n1+n2)
        ts[ii] = 2*n1/(n1+n2)
        
        # Compose transfer matrix
        M[:,:,ii] = np.dot([[np.exp(-1j*d[ii]),0],
                            [0,np.exp(1j*d[ii])]],
                           [[1, rs[ii]],[rs[ii],1]]) * 1/ts[ii]

        # Multiply with full matrix (if exists)
        if ii >= 1:
            Mt = np.dot(Mt,M[:,:,ii])
        else:
            Mt = M[:,:,0]

    # Reflection and transmission coefficients
    r = Mt[1,0]/Mt[0,0]
    t = 1/Mt[0,0]

    # Initiate arrays
    v1 = np.zeros(len(fullw),dtype=complex)
    v2 = np.zeros(len(fullw),dtype=complex)
    v1[0] = 1
    v2[0] = r

    for ii in range(1,N):
        # Coefficients
        vw = np.linalg.solve(M[:,:,ii-1], [v1[ii-1],v2[ii-1]])
        v1[ii] = vw[0]
        v2[ii] = vw[1]

        # Location array
        xloc = np.arange(0,fullw[ii],5)

        # Electric fields
        Eloc1 = v1[ii]*np.exp(1j*2*np.pi/wvl*fulln[ii]*xloc)
        Eloc2 = v2[ii]*np.exp(-1j*2*np.pi/wvl*fulln[ii]*xloc)

        # Append to arrays
        x = np.hstack((x,xloc+sum(fullw[:ii])))
        E = np.hstack((E,(Eloc1+Eloc2)))
        Nn = np.hstack((Nn,fulln[ii]+(xloc*0)))

    # Sort arrays()
    ix = np.argsort(x)
    x = x[ix]
    E = E[ix]
    Nn = Nn[ix]

    return r, t, x, Nn, E

######################################
## Example DBR

if __name__ == "__main__":
    
    # Wavelength (in nm)
    wvl = 1000

    # Refractive indices
    n2 = 1.38
    n1 = 2.32
    n0 = 1
    ns = 1.5

    # Number of layers
    Nstk = 4

    # Mirror stack n and width
    Mirrn = np.tile([n1,n2],Nstk)
    Mirrw = np.tile([wvl/(4*n1),wvl/(4*n2)],Nstk)

    # Add air and substrate
    fulln = np.insert([1,n0,ns],2,Mirrn)
    fullw = np.insert([0,wvl/n0,wvl/ns],2,Mirrw)

    # Run transfer matrix function
    r,t,x,Nn,E = tmm(wvl,fulln, fullw)

    # Units in um and offset
    x = x/1e3-1

    # Plot n and E
    fig, ax = plt.subplots(2,1,sharex=True)
    ax[0].plot(x,Nn,'b')
    ax[0].set_ylabel('Refractive index n')
    ax[0].set_title('r = %.5f, t = %.5f' %(abs(r),abs(t)))
    ax[1].plot(x,abs(E)**2,'r')
    ax[1].set_ylabel('Normalized |E|^2')
    ax[1].set_xlabel('Distance (um)')
    ax[1].set_xlim([min(x),max(x)])

    # Redefine (fixed) mirror
    Mirrw = np.tile([107.7586,181.1594],Nstk)
    fullw = np.insert([0,1000,666.6667],2,Mirrw)

    # Wavelengths array
    wvls = np.linspace(wvl-600,wvl+600,301)

    # Loop through wavelengths
    R = []
    for ii in range(len(wvls)):
        r,t,x,Nn,E = tmm(wvls[ii],fulln, fullw)
        R.append(abs(r)**2 * 100)

    # Plot reflectance vs wvls
    plt.figure()
    plt.plot(wvls,R,'b')
    plt.ylabel('Reflectance (%)')
    plt.xlabel('Wavelength (nm)')
    plt.xlim(min(wvls),max(wvls))
    plt.ylim(0,100)
    
    plt.show()
