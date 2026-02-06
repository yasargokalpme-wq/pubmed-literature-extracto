"""
PubMed Literature Extractor
Extracts article metadata from PubMed using NCBI E-utilities API
"""

from Bio import Entrez
import pandas as pd

# Configuration
Entrez.email = "yasar.gokalp.me@gmail.com"

def search_pubmed(search_term, max_results=50):
    """Search PubMed for articles"""
    print(f"Searching PubMed for: '{search_term}'...")
    
    handle = Entrez.esearch(
        db="pubmed",
        term=search_term,
        retmax=max_results,
        sort="pub_date"
    )
    record = Entrez.read(handle)
    handle.close()
    
    id_list = record["IdList"]
    print(f"Found {len(id_list)} articles")
    
    return id_list


def fetch_article_details(pmid_list):
    """Fetch detailed metadata for articles"""
    if not pmid_list:
        print("No PMIDs to fetch")
        return []
    
    print(f"Fetching details for {len(pmid_list)} articles...")
    
    id_string = ",".join(pmid_list)
    handle = Entrez.efetch(
        db="pubmed", 
        id=id_string, 
        rettype="xml", 
        retmode="xml"
    )
    records = Entrez.read(handle)
    handle.close()
    
    articles = []
    
    for article in records['PubmedArticle']:
        try:
            pmid = str(article['MedlineCitation']['PMID'])
            title = article['MedlineCitation']['Article']['ArticleTitle']
            journal = article['MedlineCitation']['Article']['Journal']['Title']
            
            pub_date = article['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']
            year = pub_date.get('Year', 'N/A')
            
            author_list = article['MedlineCitation']['Article'].get('AuthorList', [])
            if author_list:
                authors = ', '.join([
                    f"{a.get('LastName', '')} {a.get('Initials', '')}" 
                    for a in author_list[:3]
                ])
                if len(author_list) > 3:
                    authors += ' et al.'
            else:
                authors = 'No authors listed'
            
            abstract_data = article['MedlineCitation']['Article'].get('Abstract', {})
            abstract_text = abstract_data.get('AbstractText', ['No abstract available'])
            abstract = ' '.join(str(a) for a in abstract_text)
            
            pubmed_link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            
            article_data = {
                "PMID": pmid,
                "Title": title,
                "Authors": authors,
                "Journal": journal,
                "Year": year,
                "Abstract": abstract,
                "PubMed_Link": pubmed_link
            }
            
            articles.append(article_data)
            print(f"✓ Extracted: {title[:50]}...")
            
        except Exception as e:
            print(f"✗ Error: {e}")
            continue
    
    return articles


def save_to_excel(articles, filename="pubmed_results.xlsx"):
    """Save articles to Excel file"""
    if not articles:
        print("No articles to save")
        return
    
    df = pd.DataFrame(articles)
    df = df.drop_duplicates(subset=['PMID'])
    df = df.sort_values('Year', ascending=False)
    df.to_excel(filename, index=False)
    
    print(f"\n{'='*50}")
    print(f"SUCCESS!")
    print(f"{'='*50}")
    print(f"File: {filename}")
    print(f"Total articles: {len(df)}")
    print(f"{'='*50}\n")


def main():
    """Main function"""
    search_term = "CRISPR"
    max_results = 20
    
    pmid_list = search_pubmed(search_term, max_results)
    articles = fetch_article_details(pmid_list)
    save_to_excel(articles, filename="pubmed_results.xlsx")
    
    if articles:
        print("\nFirst 3 articles:")
        df = pd.DataFrame(articles)
        print(df[['PMID', 'Title', 'Year']].head(3))


if __name__ == "__main__":
    main()
