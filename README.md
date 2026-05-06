# AI Portfolio Chatbot Backend

이 프로젝트는 사용자의 이력서 및 포트폴리오 문서를 기반으로 질문에 답변하는  
**RAG(Retrieval-Augmented Generation) 기반 AI 포트폴리오 챗봇 백엔드**입니다.

업로드한 문서를 텍스트로 변환하고, 청크 분할 및 임베딩을 거쳐 Pinecone에 저장한 뒤,  
사용자 질문과 관련된 내용을 검색하여 LLM이 답변을 생성하는 구조로 구현했습니다.



## Project Overview

기존 이력서나 포트폴리오는 정적인 문서 형태로 전달되는 경우가 많습니다.  
이 프로젝트는 문서 기반 정보를 더 자연스럽고 직관적으로 전달하기 위해 만들었습니다.

사용자는 챗봇에게 질문을 입력하고,  
백엔드는 문서에서 관련 내용을 검색한 뒤 그 내용을 바탕으로 답변을 생성합니다.

이 프로젝트를 통해 다음과 같은 부분을 보여주는 것을 목표로 했습니다.

- 문서 기반 RAG 구조 이해 및 구현
- FastAPI 기반 API 설계
- 벡터 DB(Pinecone) 활용
- 프롬프트 기반 답변 품질 제어
- Render 배포 경험



## Main Features

- `.docx` 문서 업로드
- 문서 텍스트 추출 및 청크 분할
- OpenAI Embedding 생성
- Pinecone 벡터 저장
- 사용자 질문 기반 유사 문서 검색
- 검색 결과를 바탕으로 답변 생성
- 문서에 없는 정보는 단정하지 않도록 응답 제어
- FastAPI 기반 REST API 제공



## Tech Stack

- **Language**: Python
- **Framework**: FastAPI
- **LLM**: OpenAI
- **Vector DB**: Pinecone
- **Document Loader**: LangChain, Docx2txtLoader
- **Text Splitter**: RecursiveCharacterTextSplitter
- **Deployment**: Render
- **Version Control**: Git, GitHub



## Architecture

```text
User
  ↓
Vue Frontend
  ↓
FastAPI Backend
  ├─ Document Upload
  ├─ Chunking
  ├─ Embedding
  ├─ Pinecone Retrieval
  └─ OpenAI Response Generation
