
class Workflow:

    def __init__(self, summary_components, evidence_component, answer_component):
        self.summary_components = summary_components
        self.evidence_component = evidence_component
        self.answer_component = answer_component
        print("MuHeQA workflow",self.summary_components,self.evidence_component,self.answer_component,"ready")

    def decapitalize(self,str):
        return str[:1].lower() + str[1:]


    def process(self,request):
        question = request['question']
        print("Making question:",question,"..")

        entity_list = []
        if 'entities' in request:
            print("input entities:",request['entities'])
            for e in request['entities'].split("#"):
                values = e.split(";")
                entity_list.append({ 'id': values[0], 'name': values[1]})

        req_evidence = False
        if ('evidence' in request):
            req_evidence = request['evidence']

        # Compose Summary
        question = self.decapitalize(question)
        summary = ""
        for summarizer in self.summary_components:
            partial_summary = summarizer.get_summary(question, entity_list)
            summary += partial_summary + ". "

        result = {}
        result['question'] = question
        result['answer'] = "-"
        result['confidence'] = 0.0
        if (len(summary) > 0 ):
            # Extract Answer
            answer = self.evidence_component.get_answer(question,summary)
            result['confidence'] = answer['score']
            if (str(req_evidence).lower() == 'true'):
                result['evidence'] = answer['summary']
            # Create Reponse
            response = self.answer_component.get_response(question, answer['value'])
            result['answer'] = response

        print("Response: ", result['answer'])

        return result
