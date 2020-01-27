/* Author : jean-francois.gilles@upmc.fr
 * Date : the 29th nov 2018
 * 
 * Need DiAna plugin and the 3DSuite
 * -> Do segmentation in the 2 channels of the files (with the correct extension) and do some measures on objects found.
 */

path = getDirectory("Get Directory");
sep=File.separator;
list=getFileList(path);

ext = ".czi"; //file extension
minVolPxl = 80;
maxVolPxl = 6000;
minTresh = 100;
distance = 50.0; //nm

for(i=0; i<list.length; i++){
	title=list[i];
	if(endsWith(title, ext) ){
		run("Bio-Formats Windowless Importer", "open=["+path+sep+title+"]");
		run("Split Channels");
		//1st channel thresholding
		selectWindow("C1-"+title);
		run("3D Iterative Thresholding", "min_vol_pix="+minVolPxl+" max_vol_pix="+maxVolPxl+" min_threshold="+minTresh+" min_contrast=0 criteria_method=MSER threshold_method=STEP segment_results=All value_method=10 filtering");
		selectWindow("filtered_2");
		close();
		selectWindow("draw");
		run("Duplicate...", "title=mask1 duplicate channels=1");
		selectWindow("draw");
		close();
		//An other way with channel 1 (but problems after with Diana)
		//classicSeg("C1-"+title, "mask1");
		//fillToOne("mask1");
		//2nd channel thresholding
		classicSeg("C2-"+title, "mask2");
		fillToOne("mask2");
		//Analyse
		run("DiAna_Analyse", "img1=[C2-"+title+"] img2=[C1-"+title+"] lab1=mask2 lab2=mask1 coloc distc="+distance+" measure");
		selectWindow("ColocResults");
		saveAs("Results", path+sep+"ColocResults_"+title+".csv");
		run("Close");
		selectWindow("ObjectsMeasuresResults-A");
		saveAs("Results", path+sep+"MeasuresResults-A_"+title+".csv");
		run("Close");
		selectWindow("ObjectsMeasuresResults-B");
		saveAs("Results", path+sep+"MeasuresResults-B_"+title+".csv");
		run("Close");
		run("Close All");
	}
}

//Segmentation with isodata
function classicSeg(imageName, newName) {
	selectWindow(imageName);
	run("Duplicate...", "title="+newName+" duplicate");
	run("Median...", "radius=2 stack");
	setSlice(nSlices/2);
	setOption("BlackBackground", true);
	run("Convert to Mask", "method=IsoData background=Dark black");
}

//Fill signal to value 1 (needed with DiAna)
function fillToOne(imageName) {
	selectWindow(imageName);
	setForegroundColor(1, 1, 1);
	for(i=1; i<=nSlices;i++){
		setSlice(i);
		run("Create Selection");
		if(selectionType()>0){
			fill();
		}
		run("Select None");
	}
	//setMinAndMax(0, 3);
}
