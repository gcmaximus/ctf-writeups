import praw
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

def scrape_comments(subreddit_name, limit=10):
    # Use PRAW to access the official Reddit API
    # I'm not going to give you my creds lol
    reddit = praw.Reddit(
        client_id="",
        client_secret="",
        user_agent="",
    )

    comments = []

    for submission in reddit.subreddit(subreddit_name).hot(limit=limit):
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            comments.append(comment.body)

    return comments

def train_model(comments, initial_comments, prefix):
    documents = []

    for idx, string in enumerate(initial_comments):
        tokens = word_tokenize(string)
        documents.append(TaggedDocument(tokens, f'{prefix}{idx}'))

    for idx, comment in enumerate(comments):
        tokens = word_tokenize(comment)
        documents.append(TaggedDocument(tokens, f'{prefix}{len(initial_comments) + idx}'))

    model = Doc2Vec(documents, vector_size=100, window=5, min_count=1, workers=4, epochs=25)
    return model

if __name__ == '__main__':
    conservative_comments = scrape_comments('conservative')
    liberal_comments = scrape_comments('liberal')

    conservative_initial_comments = [
        "There’s a lot to be said for allowing a certain level of legal immigrants to come to the country and become "
        "citizens, pay into the system, raise families here etc, it’s an integral part of the economy. I would even say "
        "that in some cases, in an economy such as ours with the products we consume, we could even stand to have a small "
        "percentage of undocumented labor as well, which I think is not totally avoidable. But, all that being said, "
        "rampant illegal immigration only hurts things in the end, especially legal immigrants as well, but we need total "
        "border policy reform. Clear and non vague pathways to citizenship, extremely tight border security and "
        "surveillance of people outstaying visas, and as well humanitarian ways of deportation. We need to support a "
        "healthy level of legal immigrants migration, realistically be able to tolerate a very small amount of "
        "undocumented/seasonal labor, especially in the agricultural industry, and put a lid on the rest.",

        "Tucker demonstrating fully that he is not and has never been a journalist, the reality is as they say if Ukraine "
        "is abandoned expect Russia to move further and eventually against a NATO country that would then force the US "
        "into war. Tucker is no fan of NATO or even western civilization he would abandon them all for his America alone "
        "agenda an agenda that would lead to America no more and indeed the west no more.",

        "Liberals believe in conspiracy theories regarding a government if that government is run by good christians or "
        "similar people. Liberals call conspiracy theories as complete lies or misinformation regarding a government if "
        "that government is run by curropt, evil, and/or satanic people.",

        "And as it turns out that gun violence is generally not random, and that most gun violence can be concentrated to "
        "certain cities with high redacted population, with victims of violence being primarily black. And what happens "
        "when law enforcement actually tries to police these areas? They get thrown in jail by left wing DAs that will "
        "let criminals go free. But sure, we can pretend that guns are the issue. I suppose that's easier.",

        "Massive, exorbitant spending related mostly to Covid and other leftist fantasy projects. The Covid grift caused "
        "massive injections of printed money into their economy, and instead of paying down debt and saving, "
        "they increased spending efforts. Now the money has dried up but the spending has remained. They will almost "
        "certainly get bailed out by the federal government because the Brandon administration will not let their "
        "playground of communist policies fail on its own."
    ]

    liberal_initial_comments = [
        "Because people who are doing harm by their actions (or by failing to act) don’t want to hear it! Most people "
        "want to think that they’re good people, and therefore become fragile at the suggestion that they might be "
        "doing harm! So they try to turn it into something controversial. Also, those who say “both sides are the "
        "same” (or similar) usually are coming from a place of privilege or advantage! It’s usually (not always, "
        "but usually) straight white guys, because losing abortion rights, LGBT+ rights, etc doesn’t affect THEM! (Or "
        "they perceive it doesn’t). Finally, it’s NOT bullying to say these things! (It could be argued that it’s "
        "ineffective, but that’s NOT the same thing). It’s NOT automatically bullying if someone disagrees with you. "
        "Or if they point out that you’re actively doing harm. It’s uncomfortable to hear, but uncomfortable is NOT "
        "automatically bullying!",

        "Lmao, Republicans were stupid back then I thought. Banning gay marriage, putting creationism in schools, "
        "attacking Obama’s handling of the recession (despite wanting to return to the policies that started it), "
        "attacking Obamacare (despite having no alternative), and criticizing Obama’s Middle East policy when most of "
        "it wouldn’t be relevant if it weren’t for the Bush administration. People forget that our government was "
        "dysfunctional back then due to the Republican Congress. It’s easy to see how they turned into the MAGA "
        "party. Fox news is the only reason the GOP didn’t do as bad as they should have, and I suspect the only "
        "reason they ever recovered from the Bush Administration.",

        "So by not letting abortions woman may ruin their bodies if there is an issue with the baby and take away a "
        "woman’s ability to have future kids???? The GOP belief is so out of touch and really impede on a woman’s "
        "freedom. They will continue to lose overall in the nation due to their extreme beliefs",

        "They don't believe any of that. The GOP is just saying what their voters want to hear. They are trying to "
        "hold on to the dwindling base they have left that ekes them into the slimmest of majorities. The reason they "
        "are concealing their identities is because they know the people filmed are absolutely right wing nutjobs but "
        "those nutjobs voted for them. They cannot afford to lose voters because they went to prison for a felony. "
        "Ironically most states have banned felons from voting, which was meant to work the opposite way originally.",

        "Trump's profound ignorance of history and his lack of understanding the world was readily apparent prior to "
        "this statement. If anyone was delusional enough to think that a new or renewed war wasn't a Republican "
        "priority would also have a profound ignorance of history. Republicans are elected to start wars against "
        "brown-skinned nations and discriminate against the brown-skinned citizens back home. This is what "
        "Republicans do and why people vote for Republicans. Are people still in denial about this?"

    ]

    conservative_model = train_model(conservative_comments, conservative_initial_comments, 'r')

    liberal_model = train_model(liberal_comments, liberal_initial_comments, 'l')

    conservative_model.save("conservative_model.d2v")
    liberal_model.save("liberal_model.d2v")
