SELECT
	appearDate AS �W�[���,
	applyCnt AS �ӽФH��,
	coIndustryDesc AS ���~,
	custName AS ���q�W��,
	description,
	LEFT(jobAddrNoDesc,3) ����,
	jobName AS ¾��,
	jobNo AS �u�@�s��,
	jobType AS �u�@���A,
	lat as �g��,
	lon as �n��,
	major,
	optionEdu AS �Ǿ��n�D,
	remoteWorkType AS �O�_���Z,
	salaryHigh AS �~��W��,
	salaryLow AS �~��U��,
	d3 AS �u�@�ɬq,
	jobCat as ¾�Ȥ����N�X,
	isActivelyHiring AS �O�_�n���x�~
INTO [104_cleaned_2025-07-10]
FROM [104_rawdata_2025-07-10];