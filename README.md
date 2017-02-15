PLUGIN ECOCOMPTEUR DE CHEZ LEGRAND#

# Purpose

This is a package for Domogik : http://www.domogik.org

Domogik is an open source home automation solution.

# Documentation 

You can find the documentation source in the **docs/** folder. When the package will be installed, the documentation will be available in the **Documentation** menu of the Domogik administration for this package.
You may also find online documentation for this plugin. You will be able to find the documentation url on http://repo-public.domogik.org/dashboard

# Install the package

To install this package on your Domogik system, you can go in this GitHub repository releases page and get the link to a release .zip file. Then you just have to do :

    dmg_package -i http://path.to/the/file.zip

# INFO 
	
format json retourner par l'écocompteur : 
{
    "data1":66.000000,
    "data2":42.000000,
    "data3":12.000000,
    "data4":2.000000,
    "data5":292.000000,
    "data6":0.967000,
    "data6m3":0.967000,
    "data7":0.000000,
    "data7m3":0.000000,
    "heure":17,
    "minute":15,
    "CIR1_Nrj":0.000000,
    "CIR1_Vol":0.000000,
    "CIR2_Nrj":0.000000,
    "CIR2_Vol":0.000000,
    "CIR3_Nrj":0.000000,
    "CIR3_Vol":0.000000,
    "CIR4_Nrj":0.000000,
    "CIR4_Vol":0.000000,
    "Date_Time":1487178927
}