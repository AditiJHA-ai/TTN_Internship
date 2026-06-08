from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
 
#Dataset
texts = [
    # sci.space (20 samples)
    "NASA launched a new rocket to the International Space Station.",
    "Astronomers discovered a black hole at the edge of the Milky Way.",
    "The Mars rover collected soil samples from the red surface.",
    "SpaceX completed its first crewed mission to low Earth orbit.",
    "Hubble telescope captured images of a distant nebula.",
    "The lunar module landed successfully near the south pole of the Moon.",
    "Satellite imagery revealed new details about Jupiter's storm systems.",
    "Scientists detected gravitational waves from two merging neutron stars.",
    "A new exoplanet was found in the habitable zone of a distant star.",
    "The James Webb telescope peers deeper into the universe than ever before.",
    "Astronauts conducted a six-hour spacewalk to repair the solar panels.",
    "The rocket booster successfully returned to the launch pad and landed.",
    "Astronomers captured the first image of a supermassive black hole.",
    "The space probe reached the outer edges of the solar system.",
    "Scientists are developing a propulsion system for deep space travel.",
    "The new space telescope will study dark matter and dark energy.",
    "The asteroid passed within 20000 kilometres of the Earth's surface.",
    "The satellite was deployed into geostationary orbit above the equator.",
    "Cosmic radiation poses a serious challenge for long-duration space missions.",
    "The agency plans to return humans to the lunar surface by 2028.",
 
    # sci.med (20 samples)
    "The surgeon performed a successful heart bypass operation.",
    "Researchers found a new vaccine candidate for influenza.",
    "Clinical trials showed the drug reduced tumour size by 40 percent.",
    "The patient was diagnosed with Type 2 diabetes and prescribed metformin.",
    "A study linked high cholesterol to increased risk of stroke.",
    "The hospital introduced robotic-assisted surgery for precision procedures.",
    "Scientists mapped the entire human genome in a landmark study.",
    "The antibiotic was effective against multiple drug-resistant strains.",
    "MRI scans revealed damage to the patient's frontal lobe.",
    "A new blood test can detect cancer up to four years before symptoms.",
    "The WHO declared the outbreak a global health emergency.",
    "Gene therapy trials showed promising results for sickle cell disease.",
    "A clinical study found the new medication reduces blood pressure effectively.",
    "Doctors recommended surgery to remove the benign tumour from the lung.",
    "The hospital adopted a new protocol for treating sepsis in ICU patients.",
    "Researchers identified a genetic mutation linked to early-onset Alzheimer's.",
    "The antiviral drug shortened the duration of the illness by three days.",
    "Immunotherapy has shown strong results in treating melanoma patients.",
    "Surgeons successfully transplanted a kidney from a donor to a recipient.",
    "The new diagnostic tool can detect Parkinson's disease in early stages.",
 
    # rec.sport.hockey (20 samples)
    "The team scored three goals in the third period to win the Stanley Cup.",
    "The goalie made 42 saves in a remarkable shutout performance.",
    "He was penalised for high-sticking in the second period.",
    "The trade deadline saw three forwards moved to playoff contenders.",
    "The puck deflected off the defenceman's skate into the net.",
    "The coach pulled the goalie with two minutes left in regulation.",
    "The power play unit converted on all three opportunities tonight.",
    "A hat trick by the centre gave the team a commanding lead.",
    "The hockey player signed a seven-year contract extension.",
    "The referee called a penalty shot after the defender tripped the shooter.",
    "The overtime goal ended the longest playoff game in franchise history.",
    "The winger fired a slap shot from the blue line past the goaltender.",
    "The team was eliminated after losing game seven in overtime.",
    "The rookie centre won the Calder Trophy for best first-year player.",
    "A fight broke out near the boards after a late hit on the defenceman.",
    "The team went on a ten-game winning streak to clinch the division title.",
    "The captain lifted the trophy after the final buzzer sounded.",
    "The arena sold out for the seventh consecutive home game this season.",
    "The coach benched the veteran forward after a series of turnovers.",
    "The expansion team secured the first overall pick in the draft lottery.",
 
    # talk.politics.guns (20 samples)
    "The senator proposed new legislation restricting firearm purchases.",
    "Gun control advocates rallied outside the state capitol building.",
    "The Supreme Court ruled on the right to bear arms under the Second Amendment.",
    "Background checks were proposed as a requirement for all gun sales.",
    "The sheriff opposed the new ordinance limiting concealed carry permits.",
    "Lawmakers debated red flag laws that allow temporary weapon seizure.",
    "The NRA lobbied against the proposed assault weapons ban.",
    "A new bill would require gun owners to store firearms in locked safes.",
    "The debate over magazine capacity limits divided the legislature.",
    "Self-defence laws vary widely between different states in the US.",
    "The police union supported expanded background check legislation.",
    "Gun violence statistics were cited throughout the congressional hearing.",
    "The governor signed the new firearm registration bill into law.",
    "Protesters gathered outside the statehouse to oppose the gun legislation.",
    "The court struck down the city's ban on semi-automatic rifles.",
    "Legislation to close the gun show loophole was passed by the Senate.",
    "The politician argued that armed citizens deter crime in urban areas.",
    "A bipartisan group of senators introduced a compromise gun safety bill.",
    "The state legislature overrode the governor's veto on the firearms bill.",
    "Public opinion polls show divided views on stricter gun control measures.",
]
 
labels = (
    ["sci.space"] * 20 +
    ["sci.med"] * 20 +
    ["rec.sport.hockey"] * 20 +
    ["talk.politics.guns"] * 20
)
 
#Train / test split
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=42, stratify=labels
)
print(f"Training samples : {len(X_train)}")
print(f"Test samples     : {len(X_test)}")
print(f"Categories       : sci.space, sci.med, rec.sport.hockey, talk.politics.guns")
 
# --- 3. Build pipeline ---
# TfidfVectorizer: converts raw text to a matrix of TF-IDF features.
#   - max_features: keeps the top N most frequent terms
#   - stop_words: removes common words like "the", "is", "and"
#   - ngram_range: (1,2) includes single words AND two-word phrases
# MultinomialNB: Naive Bayes classifier, well-suited for word-count features.
pipeline = Pipeline([
    ("tfidf",      TfidfVectorizer(max_features=5000, stop_words="english", ngram_range=(1, 2))),
    ("classifier", MultinomialNB(alpha=0.1)),
])
 
#Train
print("\nTraining classifier...")
pipeline.fit(X_train, y_train)
 
#Evaluate on test set
predictions = pipeline.predict(X_test)
accuracy    = accuracy_score(y_test, predictions)
 
print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)\n")
print("Classification report:")
print(classification_report(y_test, predictions, zero_division=0))
 
#Predict on custom sentences
print("--- Custom predictions ---")
custom_texts = [
    "NASA launched a new rocket to orbit the International Space Station.",
    "The surgeon performed a heart bypass operation on the patient.",
    "The team scored three goals in the third period to win the Stanley Cup.",
    "The senator proposed new legislation restricting firearm purchases.",
    "Astronomers discovered a black hole at the edge of the Milky Way.",
    "The vaccine reduced the risk of infection by 90 percent in the trial.",
    "The goalie stopped a penalty shot in sudden death overtime.",
    "Congress debated whether to expand background checks for gun buyers.",
]
preds = pipeline.predict(custom_texts)
for text, label in zip(custom_texts, preds):
    print(f"  [{label:<25}]  {text[:70]}")
