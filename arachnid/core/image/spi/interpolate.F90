
C ---------------------------------------------------------------------------
		SUBROUTINE INTERPOLATE_BI_3(Q1,Q2,NX,NY,NZ,NX1,NY1,NZ1)

		REAL 						:: Q1(NX,NY,NZ)
		REAL 						:: Q2(NX1,NY1,NZ1)
		DOUBLE PRECISION 			:: PX,PY,PZ,RX,RY,RZ
		DOUBLE PRECISION 			:: TMP1,TMP2,TMP3

cf2py threadsafe
cf2py intent(inout) :: Q1,Q2
cf2py intent(in) :: NX,NY,NZ,NX1,NY1,NZ1
cf2py intent(hide) :: NX,NY,NZ,NX1,NY1,NZ1

C       REMAINING CASES
		RX = DBLE((FLOAT(NX-1))-0.0001)/FLOAT(NX1-1)
		RY = DBLE((FLOAT(NY-1))-0.0001)/FLOAT(NY1-1)
		RZ = DBLE((FLOAT(NZ-1))-0.0001)/FLOAT(NZ1-1)
		PZ = 1.0
		DO IZ=1,NZ1
	           PY   = 1.0
	           IOZ  = PZ
	           DZ   = DMAX1(PZ-IOZ,1.0D-5)
	           TMP3 = (1.0D0-DZ)
	           DO IY=1,NY1
	              PX   = 1.0
	              IOY  = PY
	              DY   = DMAX1(PY-IOY,1.0D-5)
	              TMP2 = (1.0D0-DY)
		      DO IX=1,NX1
		         IOX  = PX
		         DX   = DMAX1(PX-IOX,1.0D-5)
		         TMP1 = (1.0D0-DX)
		         Q2(IX, IY, IZ)=
     &		   TMP1 * TMP2 * TMP3
     &			* Q1(IOX,IOY,IOZ)
     &		+   DX * TMP2 * TMP3
     &			* Q1(IOX+1,IOY,IOZ)
     &	  	+ TMP1 *   DY *(1.0D0-DZ)
     &			* Q1(IOX,IOY+1,IOZ)
     &		+ TMP1 * TMP2 * DZ
     &			* Q1(IOX,IOY,IOZ+1)
     &		+   DX *   DY *TMP3
     &			* Q1(IOX+1,IOY+1,IOZ)
     &		+   DX * TMP2 * DZ
     &			* Q1(IOX+1,IOY,IOZ+1)
     &		+ TMP1 *   DY * DZ
     &			* Q1(IOX,IOY+1,IOZ+1)
     &		+   DX *   DY * DZ
     &			* Q1(IOX+1,IOY+1,IOZ+1)

		         PX = PX+RX
		      ENDDO
		      PY = PY + RY
		   ENDDO
		   PZ = PZ + RZ
		ENDDO

		END
