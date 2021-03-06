

! ---------------------------------------------------------------------------
		SUBROUTINE INTERPOLATE_FS_2(BUF1,NXLD,NY,BUF2,NX2,NY2,NX,IRTFLG)
		REAL              :: BUF1(NXLD,NY)
        REAL              :: BUF2(NX2,NY2)
        INTEGER			  :: NXLD,NY,NX2,NY2,NX,IRTFLG

!f2py threadsafe
!f2py intent(inout) :: BUF1,BUF2
!f2py intent(in) :: NXLD,NX,NY,NX2,NY
!f2py intent(hide) :: NXLD,NY,NX2,NY
!f2py intent(out) :: IRTFLG

			CALL INTERP_FBS(BUF1,BUF2,NXLD,NX,NY,NX2,NY2,IRTFLG)

		END

! ---------------------------------------------------------------------------
		SUBROUTINE INTERPOLATE_FS_3(BUFIN,NXLD,NY,NZ,BUFOUT,NX2,NY2,NZ2,NX)
        REAL              :: BUFIN (NXLD, NY,  NZ)
        REAL              :: BUFOUT(NX2,  NY2, NZ2)
        INTEGER			  :: NXLD,NY,NZ,NX2,NY2,NZ2,NX

!f2py threadsafe
!f2py intent(inout) :: BUFIN,BUFOUT
!f2py intent(in) :: NXLD,NY,NZ,NX2,NY2,NZ2,NX
!f2py intent(hide) :: NXLD,NY,NZ,NX2,NY2,NZ2

		CALL INTERP_FBS3(BUFIN,BUFOUT,NX,NY,NZ, NX2,NY2,NZ2, NXLD)

		END
! ---------------------------------------------------------------------------
		SUBROUTINE FINTERPOLATE2(X,LSD,NROW,Y,LSD2,NROW2,NSAM,NSAM2)
		REAL   			  :: X(LSD,NROW), Y(LSD2,NROW2)
        INTEGER			  :: LSD,NROW,LSD2,NROW2,NSAM,NSAM2

!f2py threadsafe
!f2py intent(inout) :: X,Y
!f2py intent(in) :: NSAM,NROW,NSAM2,NROW2,LSD,LSD2
!f2py intent(hide) :: NROW,NROW2,LSD,LSD2

			CALL FINT(X, Y, NSAM, NROW, NSAM2, NROW2, LSD, LSD2)
		END

! ---------------------------------------------------------------------------
		SUBROUTINE FINTERPOLATE3(X3,LSD,NROW,NSLICE,Y3,LSDN,NROWN,NSLICEN,NSAM,NSAMN)
        REAL   			  :: X3(LSD,NROW,NSLICE), Y3(LSDN,NROWN,NSLICEN)
        INTEGER			  :: LSD,NROW,NSLICE,LSDN,NROWN,NSLICEN,NSAM,NSAMN

!f2py threadsafe
!f2py intent(inout) :: X3,Y3
!f2py intent(in) :: NSAM,NROW,NSLICE,NSAMN,NROWN,NSLICEN,LSD,LSDN
!f2py intent(hide) :: LSD,NROW,NSLICE,LSDN,NROWN,NSLICEN

			CALL FINT3(X3,Y3,NSAM,NROW,NSLICE,NSAMN,NROWN,NSLICEN,LSD,LSDN)

		END

! ---------------------------------------------------------------------------
		SUBROUTINE INTERPOLATE_BI_3(Q1,Q2,NX,NY,NZ,NX1,NY1,NZ1)

		REAL 						:: Q1(NX,NY,NZ)
		REAL 						:: Q2(NX1,NY1,NZ1)
		DOUBLE PRECISION 			:: PX,PY,PZ,RX,RY,RZ
		DOUBLE PRECISION 			:: TMP1,TMP2,TMP3
        INTEGER			  			:: NX,NY,NZ,NX1,NY1,NZ1

!f2py threadsafe
!f2py intent(inplace) :: Q1,Q2
!f2py intent(in) :: NX,NY,NZ,NX1,NY1,NZ1
!f2py intent(hide) :: NX,NY,NZ,NX1,NY1,NZ1

!		Fixed strange bug
		RX = DBLE((FLOAT(NX)))/FLOAT(NX1)
		RY = DBLE((FLOAT(NY)))/FLOAT(NY1)
		RZ = DBLE((FLOAT(NZ)))/FLOAT(NZ1)
!       REMAINING CASES
!		RX = DBLE((FLOAT(NX-1))-0.0001)/FLOAT(NX1-1)
!		RY = DBLE((FLOAT(NY-1))-0.0001)/FLOAT(NY1-1)
!		RZ = DBLE((FLOAT(NZ-1))-0.0001)/FLOAT(NZ1-1)
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
		         Q2(IX, IY, IZ)= &
     		   TMP1 * TMP2 * TMP3 &
     			* Q1(IOX,IOY,IOZ) &
     		+   DX * TMP2 * TMP3 &
     			* Q1(IOX+1,IOY,IOZ) &
     	  	+ TMP1 *   DY *(1.0D0-DZ) &
     			* Q1(IOX,IOY+1,IOZ) &
     		+ TMP1 * TMP2 * DZ &
     			* Q1(IOX,IOY,IOZ+1) &
     		+   DX *   DY *TMP3 &
     			* Q1(IOX+1,IOY+1,IOZ) &
     		+   DX * TMP2 * DZ &
     			* Q1(IOX+1,IOY,IOZ+1) &
     		+ TMP1 *   DY * DZ &
     			* Q1(IOX,IOY+1,IOZ+1) &
     		+   DX *   DY * DZ &
     			* Q1(IOX+1,IOY+1,IOZ+1)

		         PX = PX+RX
		      ENDDO
		      PY = PY + RY
		   ENDDO
		   PZ = PZ + RZ
		ENDDO

		END

