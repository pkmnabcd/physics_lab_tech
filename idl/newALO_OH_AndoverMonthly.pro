pro newALO_OH_AndoverMonthly ; c:\

;Set the day numbers for automatic running
daynum = strarr(501)
for j = 0,500 do begin
	daynum[j] = string(j)
endfor

endfile = '*.tif'       ; Use this with raw data

daysArray = list('01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '09-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22', '22-23', '23-24', '24-25', '25-26', '26-27', '27-28', '28-29', '29-30', '30-31', '28-01', '29-01', '30-01', '31-01')

foreach day, daysArray do begin

; images location end in \
yearl = '2016'
month = 'Aug'           ; First 3 letters, capitalized
date = month+day

drive = 'I:\'
subfolder = 'ChileMTM\'+yearl+'\'+month+''+yearl+'\'                   ; Use this with raw data
location = drive + subfolder + date

; output images
site = 'ALO'
year = '16'
out_dir = drive+'ChileMTM\'+yearl+'\'+month+''+yearl+'\processed\'

;'zenith center + box size
centerx = 63
centery = 63
box = 2
box_size = box * 2 + 1
box_pix = box_size * box_size

;Image dimensions
;Original Image
;dim1 = 128
;Display Size
;dim2 = 256

; for displaying graphs
;window, 0, xpos = 0, ypos = 0, xsize = 1000, ysize = 500
;!p.multi = [0,4,2]  ;3x4 graphs


; ******************************* OH Temperature Andover ****************************************

;//////////////////////////////////////////////////// P2 Intensities  ///////////////////////////

	print, location+'\P12A' + endfile
	file = FINDFILE(location+'\P12A' + endfile,count=nf)
  if (nf le 0) then print,'could not find the P12 data'


	n2 = n_elements(file)
	p2 = fltarr(n2)
	p2time = fltarr(n2)
	p2CCDTemp = fltarr(n2)


	if n2 gt 5 then begin
		for i = 0,n2-1 do begin
			st = 0.
			a = read_tiff(file[i])
			for x = centerx - box, centerx + box do begin
				for y = centery - box, centery + box do begin
					st = st + a[x,y]
				endfor
			endfor
			p2[i] = st/box_pix

			; to display images
			;c = rebin(a, dim2,dim2)
			;tv, bytscl(c, min = 10000, max = 30000), 0

			hr2 = read_binary(file[i], data_start =247 , data_type = 3, data_dims = [9])
			p2hour = string(hr2[2])
			p2minute = string(hr2[1])
			p2second = string(hr2[0])
			p2time[i] = p2hour + p2minute/60. + p2second/3600.
			for o = 0,n2-1 do begin
				if p2time[o] gt 12. then p2time[o] = p2time[o] - 24.
			endfor
			p2CCDTemp[i] = read_binary(file[i], data_start =306 , data_type = 4, data_dims = 0)
		endfor
	endif
	plot, p2time, p2, xrange = [-12,12],  /ynozero, title='P12'; yrange = [5000,30000]

	;//////////////////////////////////////  P4 Intensities   ///////////////////////////////////////
	file = FINDFILE(location+'\P14A' + endfile)
	n3 = n_elements(file)
	p4 = fltarr(n3)
	p4time = fltarr(n3)

	if n3 gt 5 then begin
		for i = 0,n3-1 do begin
			st = 0.
			a = read_tiff(file[i])
			for x = centerx - box, centerx + box do begin
				for y = centery - box, centery + box do begin
					st = st + a[x,y]
				endfor
			endfor
			p4[i] = st/box_pix

			hr2 = read_binary(file[i], data_start =247 , data_type = 3, data_dims = [9])
			p4hour = string(hr2[2])
			p4minute = string(hr2[1])
			p4second = string(hr2[0])
			p4time[i] = p4hour + p4minute/60. + p4second/3600.
			for o = 0,n3-1 do begin
				if p4time[o] gt 12. then p4time[o] = p4time[o] - 24.
			endfor
		endfor
	endif
	plot, p4time, p4, xrange = [-12,12],  title = 'P14', /ynozero

	;///////////////////////////////////////////////////// BG Intensities ////////////
	file = FINDFILE(location+'\BG' + endfile)
	n4 = n_elements(file)
	bg = fltarr(n4)
	bgtime = fltarr(n4)
	bd = fltarr(n4)

	if n4 gt 5 then begin
		for i = 0,n4-1 do begin
			st = 0.
			;print, file[i]
			a = read_tiff(file[i])
			for x = centerx - box, centerx + box do begin
				for y = centery - box, centery + box do begin
					st = st + a[x,y]
				endfor
			endfor
			bg[i] = st/box_pix
			hr2 = read_binary(file[i], data_start =247 , data_type = 3, data_dims = [9])
			bghour = string(hr2[2])
			bgminute = string(hr2[1])
			bgsecond = string(hr2[0])
			bgtime[i] = bghour + bgminute/60. + bgsecond/3600.
			for o = 0,n4-1 do begin
				if bgtime[o] gt 12. then bgtime[o] = bgtime[o] - 24.
			endfor
		endfor
	endif
	plot, bgtime, bg, xrange = [-12,12], yrange = [0,15000], title = 'BG'

	;//////////////////////////////////////////// DARK Intensities //////////////////
	file = FINDFILE(location+'\Dark' + endfile)
	n5 = n_elements(file)
	dk = fltarr(n5)
	dktime = fltarr(n5)
	dk = fltarr(n5)
	dkavg=0.

 ; n5=9 ; used for when there are bad Dark images in folder. Delete bright ones and n5 is number of Dark_sr*.tif files in folder
	if n5 gt 5 then begin
		for i = 0,n5-1 do begin
			st = 0.
			;print, file[i]
			a = read_tiff(file[i])
			for x = centerx - box, centerx + box do begin
				for y = centery - box, centery + box do begin
					st = st + a[x,y]
				endfor
			endfor
			dk[i] = st/box_pix
			hr2 = read_binary(file[i], data_start =247 , data_type = 3, data_dims = [9])
			dkhour = string(hr2[2])
			dkminute = string(hr2[1])
			dksecond = string(hr2[0])
			dktime[i] = dkhour + dkminute/60. + dksecond/3600.
			for o = 0,n5-1 do begin
				if dktime[o] gt 12. then dktime[o] = dktime[o] - 24.
			endfor
			;print, dktime[i], dk[i]
			dkavg=dkavg+dk[i]
		endfor
	endif
	dkavg=dkavg/n5
	plot, dktime, dk, xrange = [-12,12], /ynozero, title = 'Dark'

	;/////////interpolate all filters to P12 time ////////////
	if n2 gt 5 then begin
	splp2 = fltarr(n2)
	splp2 = spline(p2time, p2, p2time, .1)
	splp4 = fltarr(n2)
	splp4 = spline(p4time, p4, p2time, .1)
	splbg = fltarr(n2)
	splbg = spline(bgtime, bg, p2time, .1)
	spldk = fltarr(n2)
	spldk = spline(dktime, dk, p2time, .1)

	; temp using actual dark zenith values
	ohtemp = fltarr(n2)
	ohtemp = 228.45/$
           [alog(2.810*[[(splp2 - dkavg) - .733*(splbg - dkavg)]/$
           [[[(splp4 - dkavg) - .694*(splbg - dkavg)]]]])]              
  ohtemp = ohtemp + .62 + .0179*(ohtemp - 150) + .000616*(ohtemp - 150)^2

	plot, p2time, p2CCDTemp, xrange = [-12,12], yrange = [-50,-60], title='CCD Temp'
	plot, p2time, ohtemp, xrange = [-12,12], /ynozero, title='OH Temp'

	bandi = fltarr(n2)
	bandi = (6.80 + 0.069*(ohtemp-150) - 0.00019*(ohtemp - 150)^2)*(splp2 -.72*splbg)
	p2time = fix(p2time*100) / 100.0

	plot, p2time, bandi, xrange = [-12,12], /ynozero ,title='OH Band Int'

	openw, 2, out_dir +'OH_Andover_'+site+year +'day'+ strcompress(string(hr2[7]+1),/remove_all)+ '.dat'
	printf,2,FORMAT='(8A15)', date+'-'+year, 'OHTemp','OHBandInt','CCDTemp','P12','P14','BG','ActDark'
	for o = 0,n2-1 do begin
		printf, 2, format='(8f15.4)',p2time[o], ohtemp[o],  bandi[o], p2CCDTemp[o], splp2[o], splp4[o], splbg[o], spldk[o] ; changed by yucheng,5/5/10
	endfor
	close, 2
endif


;/////////////////////////////////// O2 Temperature Andover    /////////////////////////////////////

	;//////////////////////////////////////  866 Intensities   ///////////////////////////////////////
	file = FINDFILE(location+'\866A_sr' + endfile)


	n6 = n_elements(file)
	e866 = fltarr(n6)
	e866time = fltarr(n6)

	if n6 gt 5 then begin
		for i = 0,n6-1 do begin
			st = 0.
			;print, file[i]
			a = read_tiff(file[i])
			for x = centerx - box, centerx + box do begin
				for y = centery - box, centery + box do begin
					st = st + a[x,y]
				endfor
			endfor
			e866[i] = st/box_pix   ;(box*2+1)^2.

			hr2 = read_binary(file[i], data_start =247 , data_type = 3, data_dims = [9])
			e866time[i] = string(hr2[2]) + string(hr2[1])/60. + string(hr2[0])/3600.
			for o = 0,n6-1 do begin
				if e866time[o] gt 12. then e866time[o] = e866time[o] - 24.
			endfor
		endfor
	endif

	;//////////////////////////////////////  846 Intensities   ///////////////////////////////////////
	file = FINDFILE(location+'\868A_sr' + endfile)
	n7 = n_elements(file)
	e868 = fltarr(n7)
	e868time = fltarr(n7)

	if n7 gt 5 then begin
		for i = 0,n7-1 do begin
			st = 0.
			;print, file[i]
			a = read_tiff(file[i])
			for x = centerx - box, centerx + box do begin
				for y = centery - box, centery + box do begin
					st = st + a[x,y]
				endfor
			endfor
			e868[i] = st/box_pix

			hr2 = read_binary(file[i], data_start =247 , data_type = 3, data_dims = [9])
			e868time[i] = string(hr2[2]) + string(hr2[1])/60. + string(hr2[0])/3600.
			for o = 0,n7-1 do begin
				if e868time[o] gt 12. then e868time[o] = e868time[o] - 24.
			endfor
		endfor
	endif


;************************** O2 Temperature Andover *******************************************
i=0
c = 0.170		;Bill's factor
b = 3.288e-3	;Bill's factor
a = -7.377e-6	;Bill's factor

if n6 gt 5 then begin

	splbg = fltarr(n6)
	splbg = spline(bgtime, bg, e866time, .1)
	spldk = fltarr(n6)
	spldk = spline(dktime, dk, e866time, .1)
	spl866 = fltarr(n6)
	spl866 = spline(e866time, e866, e866time, .1)
	spl868 = fltarr(n6)
	spl868 = spline(e868time, e868, e868time, .1)


	; temp using actual dark zenith values
	o2temp = fltarr(n6)
	bandi2 = fltarr(n6)
	Trc = fltarr(n6)
  r = fltarr(n6)
	
	;Trc = (248.9 * r + 77.7)

  ; New equation for O2 temperature 12-02-04
  S1c =         (spl866 - dkavg) - 0.580 * (splbg - dkavg)
  S2c = 1.013 * [(spl868 - dkavg) - 0.571 * (splbg - dkavg)]
  r = S2c / S1c

  o2temp = (248.9 * r + 77.7)

  bandi2 = (3.453 + 0.00655* o2temp) * (S1c + 1.013 * S2c)
  

	plot, e866time, o2temp, xrange = [-12,12], /ynozero, title='O2 Andover Temp'

	plot, e866time, bandi2, xrange = [-12,12], /ynozero ,title='O2 Andover Band Int'


	openw, 1, out_dir +'O2_Andover_'+site+year +'day'+ strcompress(string(hr2[7]+1),/remove_all)+ '.dat'
	for o = 0,n6-2 do begin
		printf, 1, format='(7f15.6)',e866time[o], o2temp[o],  bandi2[o], spl866[o], spl868[o], splbg[o], spldk[o]; Yucheng, 5/5/10
	endfor
	close, 1
endif
endforeach
stop
end
