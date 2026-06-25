        """
        :param gammac (int): Main axis of the line: (1) East-West; (2) North-South.
        :param theta (float): Angle between line and wind in degrees.

        
       
        """
        
        # function [I]=CIGREMOD_general_ampacidad(Ta,Vw,ID,theta,y,gammac,lat,D,d2,r,e,alfa,Tc,r2,ang,fecha)
        # VARIABLES
        #% Ta=temperatura ambiente en ºC
        #% Vw=velocidad de viento m/s
        #% theta=Ángulo entre el viento y el conductor en grados
        #% y=altura del conductor sobre el nivel del mar en m
        #% gammac=dirección de la línea Este-Oeste(1) o Norte-Sur(2)
        #% lat=latitud del conductor en grados
        #% N=día del año
        #% hora=hora del día
        #% D=diametro del conductor m
        #% d2=diametro de los cables de la capa exterior en m 
        #% r=coeficiente de resistencia por grado en 1/C
        #% coef=coeficiente de dilatación a 20 ºC
        #% e=emisisvidad del conductor
        #% alfa=absortividad del conductor
        #% ID=radiación en W/m^2
        #% Tc=temperatura del conductor en ºC
        #% Imed= intensidad medida en el conductor en A
        #% r2= resistencia del conductor a 20 ºC en Ohmios
        #% r2t= resistencia del conductor a la temperatura Tc en Ohmios
        #% delta= declinación solar en grados
        #% ohmega= Ángulo horario en grados
        #% Hs= altitud solar en grados
        #% gammas= azimut del sol en grados
        #% nu= Ángulo del haz solar respecto del eje del conductor en grados
        #% Tfilm= temperatura de película en ºC
        #% Rf= coeficiente de rugosidad del conductor
        #% ror= densidad relativa del aire
        #% f= viscosidad cinemática en m^2/s
        #% Re= número de Reynolds
        #% Gr= número de Grashof
        #% Prandtl= número de Prandtl
        #% aux= reducción del ángulo theta al primer cuadrante en grados
        #% NU1= número de Nusselt
        #% Nud= número de Nusselt dependiente de la dirección del viento
        #% Nucor= número de Nusselt corregido
        #% Nun= número de Nusselt en convección natural
        #% Nu= máximo número de Nusselt
        #% lambda= conductividad térmica del aire en W/mK
        #% Pc= calor refrigerado por convección en W/m
        #% Pr= calor refrigerado por radiación en W/m
        #% Ps= calor absorvido por la radiación solar en W/m
        #% I= ampacidad en A
        #% fecha= fecha
       
        
        Ta = self.Case1.TAMB
        Vw = self.Case1.VWIND
        ID = self.Case1.SolarRadiation  # radiation in W/m^2
        theta = self.Case1.WINDANG_DEG
        y = self.Case1.CDR_ELEV
        gammac = 1  
        lat = self.Case1.CDR_LAT_DEG
        D = self.Cable1.D/1000.0 # Diameter in m
        N = self.Case1.NDAY
        d2 = 15
        r = 2
        e = self.Cable1.EMISS
        alfa = self.Cable1.ABSORP
        Tc = 3
        r2 = 2
        ang = 3
        fecha = 3
        mes = 2
        dia = 10
        hora = self.Case1.SUN_TIME
        min = 30
    
        DEG_TO_RAD = np.pi/180
       
        # Conductor resistance
        r2t=r2*(1+r*(Tc-20))
        
        # Solar heating
        N=np.round(dia+mes*30.41-30.41);
        if min>30:
            hora=hora+1;

        delta=23.4583*np.sin(DEG_TO_RAD*(284+N)*360/365)
        ohmega=(hora-12)*15
        
        
        Hs=np.arcsin( np.cos(DEG_TO_RAD*lat)*np.cos(DEG_TO_RAD*delta)*np.cos(DEG_TO_RAD*ohmega)+np.sin(DEG_TO_RAD*lat)*np.sin(DEG_TO_RAD*delta))
        if gammac == 1:
            gammac=90
        else:
            gammac=0

        gammas = np.arcsin(np.cos(DEG_TO_RAD*delta)*np.sin(DEG_TO_RAD*ohmega)/np.cos(Hs))
        nu = np.arccos( np.cos(Hs)*np.cos( DEG_TO_RAD*(gammas-gammac)))
        Ps = alfa*D*(ID*(np.sin(DEG_TO_RAD*nu)))

        # Convection cooling
        Tfilm = (Tc+Ta)/2
        Rf = d2/(2*(D-2*d2))
        ror = np.exp( -1.16e-4*y)
        f=1.32e-5+9.5e-8*Tfilm
        Re=ror*Vw*D/f
        Gr=(pow(D,3)*(Tc-Ta)*9.81)/((Tfilm+273)*(f**2))
        Prandtl=0.715-2.5e-4*Tfilm
        
        if Re>1e2 and Re<2.65e3:
            B1=0.641
            n=0.471
        elif Rf<=0.05 and Re>2.65e3 and Re<5e4: 
            B1=0.178
            n=0.633
        elif Rf>0.05 and Re>2.65e3 and Re<5e4: 
            B1=0.048
            n=0.8
        else:
            B1=0
            n=0

        Nu1=B1*pow(Re,n)
        if theta>360-ang:
            aux1=ang-(360-theta)
        else:
            aux1=theta+ang
 
        if aux1>=0 and aux1<=90:
            aux2=aux1
        elif aux1>=360 and aux1<=360+ang:
            aux2=aux1-360
        elif aux1>90 and aux1<=180:
            aux2=180-aux1
        elif aux1>180 and aux1<=270:
            aux2=aux1-180
        elif aux1>270 and aux1<360:
            aux2=360-aux1

        if aux2>=0 and aux2<=24:
            A1=0.42
            B2=0.68
            m1=1.08
        else:
            A1=0.42
            B2=0.58
            m1=0.90


        Nud=Nu1*(A1+B2*(pow(np.sin(DEG_TO_RAD*aux2),m1)))
        Nucor=0.55*Nu1
        
        if Gr*Prandtl>100 and Gr*Prandtl<10000:
            A2=0.850
            m2=0.188
        elif Gr*Prandtl>10000 and Gr*Prandtl<1000000:
            A2=0.480
            m2=0.250    
        else:
            A2=0
            m2=0 

        Nun=A2*pow(Gr*Prandtl,m2)

        Nu = np.max([Nud, Nun, Nucor])

        lambda1 = 2.42e-2+(7.2e-5)*Tfilm
        Pc = np.pi*lambda1*(Tc-Ta)*Nu
        
        
        # Radiation cooling
        Pr=np.pi*D*e*5.6704e-8*(pow(Tc+273,4)-pow(Ta+273,4))

        # Calorific capacity
        #% for s=1:length(a)
        #%      if s==1
        #%         Cp(s)=0;
        #%      else
        #%  Cp(s)=0.977*800*(Tc(s-1)-Tc)/240;
        #%      end
        #%  end
        # #%%
        #%CALCULO AMPACIDAD

        I = np.sqrt((Pc+Pr-Ps)/(r2t))

        # % plot(1:length(a),I,'*b')
        # % hold on
        # % plot(1:length(a),Imed,'*r')        

        self.Case1.QS = Ps
        self.Case1.QR = -Pr
        self.Case1.QC = -Pc