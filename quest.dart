class Question {
  String text;
  int scoreYes;
  int scoreNo;

  Question(this.text, this.scoreYes, this.scoreNo);
}

class MenstrualHealthSurvey {
  List<Question> questions;
  int totalScore = 0;

  MenstrualHealthSurvey(this.questions);

  void answerQuestion(int questionIndex, bool answerYes) {
    Question question = questions[questionIndex];
    totalScore += answerYes ? question.scoreYes : question.scoreNo;
  }

  String getResult() {
    if (totalScore <= 3) return 'Impacte lleu o cap impacte.';
    if (totalScore <= 7) return 'Impacte moderat, pot requerir una revisió mèdica.';
    return 'Impacte sever, és aconsellable buscar ajuda mèdica.';
  }
}

void main() {
  List<Question> questions = [
    Question('El teu sagnat menstrual és més freqüent que cada 21 dies?', 2, 0),
    Question('El teu sagnat menstrual dura més de 7 dies?', 2, 0),
    Question('Consideres que el teu sagnat menstrual és excessivament abundant?', 3, 0),
    Question('Pateixes dolors forts durant el teu període menstrual que interfereixen amb les teves activitats diàries?', 3, 0),
    Question('Experimentes símptomes addicionals (com ara nàusees, mal de cap intens, mareigs) durant el teu període?', 2, 0),
    Question('El teu període menstrual té un impacte negatiu en la teva vida social o emocional?', 2, 0)
  ];

  MenstrualHealthSurvey survey = MenstrualHealthSurvey(questions);

  // Exemple de com respondre a preguntes
  survey.answerQuestion(0, true); // Respondre 'Sí' a la primera pregunta
  survey.answerQuestion(1, false); // Respondre 'No' a la segona pregunta

  // Obtindre el resultat
  print(survey.getResult());
}
