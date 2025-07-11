SELECT
	appearDate AS 上架日期,
	applyCnt AS 申請人數,
	coIndustryDesc AS 產業,
	custName AS 公司名稱,
	description,
	LEFT(jobAddrNoDesc,3) 縣市,
	jobName AS 職稱,
	jobNo AS 工作編號,
	jobType AS 工作型態,
	lat as 經度,
	lon as 緯度,
	major,
	optionEdu AS 學歷要求,
	remoteWorkType AS 是否遠距,
	salaryHigh AS 薪資上限,
	salaryLow AS 薪資下限,
	d3 AS 工作時段,
	jobCat as 職務分類代碼,
	isActivelyHiring AS 是否積極徵才
INTO [104_cleaned_2025-07-10]
FROM [104_rawdata_2025-07-10];