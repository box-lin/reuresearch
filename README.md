# Android Compatibility Analysis

1. Compute the android installation/runtime compatibility for Benign apps 2018-2019 and Malware apps 2010-2019.

2. Statisticly analysis the Installation/Runtime Compatibility for RQs (1-6 see research paper)

3. Develop new computation method that computes the compatibility for multi-apk for 2018-2019 andriod apps
	
	**Installation-time**
	-	Refer to installation log
	-	For each apk that failed at installation on API X as found from the log
	-	Find all other apks that share the same package name from the large app list 
	-	For each of such found apks, install it on API X 
	-	If any of such installation succeeds, then this app (called multi-apk-compatible (MAC) app) should not be considered unable to install at API X

	**Run-time**
	-	Given an app, we run it on multiple different platforms (device configuration + API level) 
	-	If the app did not produce the ‘effects’ in at least one platform A, then we know this app probably does not have application/logic errors
	-	And then if this same app produces some of the ‘effect’s in another platform B, then we know this app is incompatible with this platform 
	-	Further, by knowing what we changed between A and B, we actually would also know that is the cause of the incompatibility
	-	The changes would be likely the following:
	-	Removing camera
	-	Change screen size
	-	Change SDK version

	**RQs (also answered for benign apps and malware separately; then we can compare between these two categories)**
	-	RQ1: Distribution of #apks per app
	-	1 for the majority of the apps
	-	Use a Histogram to present (x axis: #apks, grouped by app year), y axis: percentage)
	-	RQ2: Prevalence of MAC apps (percentage of such apps per year and per API level) - plot similarly to Figure 2 in issta paper
	-	RQ3: API level compatibility coverage of all the apks of MAC apps (essentially answer the question of how much multi-apk actually helped compatibility)
	-	E.g., originally, we considered only one apk for an app, and found it is only compatible on API X1 and API X2 (so the coverage is 2/8)
	-	Now, after considering multi-apks for this app, we found that this app is compatible on API X3, API X5 additionally (so the coverage is 4/8)
