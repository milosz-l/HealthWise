import os
import pandas as pd
from langchain_community.chat_models import ChatPerplexity, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from kg_rag.utility import system_prompts, config_data, load_chroma, load_sentence_transformer, get_prompt, retrieve_context


class KnowledgeChain:
    def __init__(self, source):
        KNOWLEDGE_PROMPT_TEMPLATE = "You are a knowledgebase. Provide general medical information about the following symptoms or conditions, referencing professional medical literature specifically from " + source + """.
User request: {rephrased_request}
Medical information:"""
        llm = ChatPerplexity(model="llama-3.1-sonar-small-128k-online", pplx_api_key=os.getenv("PERPLEXITYAI_API_KEY"))

        self.source = source
        self.chain = PromptTemplate.from_template(KNOWLEDGE_PROMPT_TEMPLATE) | llm #| StrOutputParser() # TODO: change output parser so that citations are shown


    def invoke(self, state):
        return {"source_knowledge_pairs": [(self.source, self.chain.invoke(state))]}
    

class KnowledgeChainKGRAG(KnowledgeChain):
    EDGE_EVIDENCE = False
    SYSTEM_PROMPT = system_prompts["KG_RAG_BASED_TEXT_GENERATION"]
    CONTEXT_VOLUME = int(config_data["CONTEXT_VOLUME"])
    QUESTION_VS_CONTEXT_SIMILARITY_PERCENTILE_THRESHOLD = float(config_data["QUESTION_VS_CONTEXT_SIMILARITY_PERCENTILE_THRESHOLD"])
    QUESTION_VS_CONTEXT_MINIMUM_SIMILARITY = float(config_data["QUESTION_VS_CONTEXT_MINIMUM_SIMILARITY"])
    VECTOR_DB_PATH = config_data["VECTOR_DB_PATH"]
    NODE_CONTEXT_PATH = config_data["NODE_CONTEXT_PATH"]
    SENTENCE_EMBEDDING_MODEL_FOR_NODE_RETRIEVAL = config_data["SENTENCE_EMBEDDING_MODEL_FOR_NODE_RETRIEVAL"]
    SENTENCE_EMBEDDING_MODEL_FOR_CONTEXT_RETRIEVAL = config_data["SENTENCE_EMBEDDING_MODEL_FOR_CONTEXT_RETRIEVAL"]
    TEMPERATURE = config_data["LLM_TEMPERATURE"]
    INSTRUCTION = "Context:\n\n{context} \n\nQuestion: {question}"

    def __init__(self, source='SPOKE-KG'):
        self.vectorstore = load_chroma(self.VECTOR_DB_PATH, self.SENTENCE_EMBEDDING_MODEL_FOR_NODE_RETRIEVAL)
        self.embedding_function_for_context_retrieval = load_sentence_transformer(self.SENTENCE_EMBEDDING_MODEL_FOR_CONTEXT_RETRIEVAL)
        self.node_context_df = pd.read_csv(self.NODE_CONTEXT_PATH)
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0, api_key=os.getenv("PERPLEXITYAI_API_KEY"))
        template = get_prompt(self.INSTRUCTION, self.SYSTEM_PROMPT)

        self.source = source
        self.chain = PromptTemplate(template=template, input_variables=["context", "question"]) | self.llm | StrOutputParser()


    def invoke(self, state):
        context = retrieve_context(state['rephrased_request'], self.vectorstore, self.embedding_function_for_context_retrieval, self.node_context_df,
                                   self.CONTEXT_VOLUME, self.QUESTION_VS_CONTEXT_SIMILARITY_PERCENTILE_THRESHOLD, self.QUESTION_VS_CONTEXT_MINIMUM_SIMILARITY,
                                   self.EDGE_EVIDENCE, llm_type='llama', llm=self.llm)
        state = {'question': state['rephrased_request'], 'context': context}
        return {"source_knowledge_pairs": [(self.source, self.chain.invoke(state))]}

