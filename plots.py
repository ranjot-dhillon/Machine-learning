#total meaagaes sent by user
def fetch_statstic(selected_user,df):
    if selected_user=='overall':
        return df.shape[0]
    else:
        return df[df['user']==selected_user].shape[0]

# total words sent by user
def total_words(selected_user,df):
    if selected_user=='overall':
        word=[]
        for i in df['message']:
            word.extend(i.split(' '))
        return len(word)
    else:
        new_df=df[df['user']==selected_user]
        word = []
        for i in new_df['message']:
            word.extend(i.split(' '))
        return len(word)

# Total media sent by user

def total_media(selected_user,df):
    new_df=df[df['message']=='<Media omitted>\n']
    if selected_user=='overall':
        return new_df.shape[0]

    else:
       return  new_df[new_df['user']==selected_user].shape[0]

# Number of links

from urlextract import URLExtract
extract=URLExtract()
def link(selected_user,df):
    if selected_user=='overall':
       link=[]
       for msg in df['message']:
           link.extend(extract.find_urls(msg))
       return len(link)

    else :
        new_df = df[df['user'] == selected_user]
        link = []
        for msg in new_df['message']:
            link.extend(extract.find_urls(msg))
        return len(link)







