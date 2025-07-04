-- 如果已存在，可以先刪除避免錯誤
DROP TABLE IF EXISTS [104職缺].[dbo].[jobs_104_cleaned];

-- 建立新表並篩選相關資料分析職缺，排除工程師職缺（中英皆排除）
SELECT
    jobNo,
    jobName,
    custName,
    jobAddrNoDesc AS location,
    optionEdu AS education,
    periodDesc AS experience,
    salaryLow,
    salaryHigh,
    salaryDesc,
    appearDate,
    job_category,
    coIndustryDesc AS industry,
    description,
    lon,
    lat,
    mrt,
    dist,
    isActivelyHiring
INTO [104職缺].[dbo].[jobs_104_cleaned]
FROM [104職缺].[dbo].[jobs_104_raw]
WHERE 
    (
        jobName LIKE N'%資料分析%' OR description LIKE N'%資料分析%' OR
        jobName LIKE N'%數據分析%' OR description LIKE N'%數據分析%' OR
        jobName LIKE N'%data analysis%' OR description LIKE N'%data analysis%' OR
        jobName LIKE N'%data analytic%' OR description LIKE N'%data analytic%' OR
        jobName LIKE N'%data analyse%' OR description LIKE N'%data analyse%' OR
        jobName LIKE N'%商業分析%' OR description LIKE N'%商業分析%' OR
        jobName LIKE N'%business intelligence%' OR description LIKE N'%business intelligence%' OR
        jobName LIKE N'%BI%' OR description LIKE N'%BI%'
    )


