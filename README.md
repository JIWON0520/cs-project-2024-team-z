# C&S Project 2024 - Team Z

 태아의 건강 상태를 모니터링하는 것은 임신 과정에서 매우 중요하다. 특히 태아의 심박동 수는 태아의 건강 상태를 판단하는 데 중요한 지표 중 하나로, 이상 유무를 조기에 발견하여 적절한 조치를 취할 수 있다. 이를 확인하기 위해 병원이나 전문 클리닉을 방문하는 과정에서 임산부는 위험에 노출되며, 가격 또한 회당 3~5만원 상당으로 비싸다. 따라서 본 프로젝트는 임산부가 병원 방문 없이도 태아의 심박수를 간편하게 모니터링하며, 경제적 부담 없이 건강 상태를 지속적으로 확인할 수 있는 서비스 제공을 목표로 한다.

## Project Docs

1) [Project Intention Report](https://docs.google.com/document/d/1Xdnv1-ectwGFsqLcR2frqd65CG1AkI7WiflfFV3hdWs/edit?usp=sharing)
2) [Project Plan(ppt)](https://docs.google.com/presentation/d/1xa1XNE7MeStpCspio821lLpRg6xH0q_Upz2LCIQs3TM/edit?usp=sharing)

## Directory Structure

The directory structure below must be followed, and must be periodically updated in order to be recognized for contributions in external activities such as presentations.

```
/
    /docs/
    /Dockerfile  # or, /Containerfile
    /README.md
    /Usage.md
    /...  # your own source codes
```

## Guidelines

Team members are responsible for taking on tasks appropriate to their roles and submitting them periodically to the appropriate repositories. At this time, please be aware of the following precautions.

* Prohibition of account sharing: The act of pushing someone else's work to your ID is prohibited. **You can only upload your own results with your GitHub account.**
* Periodic upload recommended: Even if the results such as code are incomplete, **please continue to push the progress so that other team members and evaluators can observe and give feedback.** The act of pushing completed results at once is recognized only as a contribution for that date, and efforts in the process are difficult to be recognized.
* Documentation recommended: Documentation in the `docs` directory provided by default will be credited to the author. In addition, even if presentation materials such as PPT are uploaded in binary format, if the contents are listed in the `docs` directory, contributions can be recognized by quoting them.
* Create a `Dockerfile (Containerfile)`: Project artifacts should be able to be packaged into one (or more) container image with the following command: `docker build --tag cs-project-2024-team-xxx .`
    - Build arguments and environment variable dependencies should not be present.
    - **Execution: Execution and usage for containerized images must be documented in `Usage.md` file.**

## Q&A

Please use the `Issues` function to raise inquiries.
