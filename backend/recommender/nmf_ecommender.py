import pandas as pd
import joblib
from config.settings import NMF_W,NMF_H,NMF_USER_INDEX,NMF_PRODUCT_INDEX,NMF_SIM_DF


# Load pre-trained artifacts

W = joblib.load(NMF_W)  #(customer id* latent factor)
H = joblib.load(NMF_H)   #( latent factor * product id)
print("sape of W",W.shape)
user_index = joblib.load(NMF_USER_INDEX) # user index cutomoer id:index
#print("sape of user_index",user_index) #
product_index = joblib.load(NMF_PRODUCT_INDEX)# product inde product id:index
sim_df = pd.read_pickle(NMF_SIM_DF)


# Recommendation functions

def recommend(customer_id=None, product_id=None, top_n=5, alpha=0):
    print("Known IDs sample:", list(user_index.keys())[:5])
    print("Incoming ID:", customer_id)

    """
    Unified recommender:
    - Known customer: personalized recommendations
    - Guest + product: item-based recommendations
    - Known customer + product click: hybrid (blend)
    
    alpha = weight for personalization (0..1)
    """
    
    # Known user
    if customer_id and customer_id in user_index:
        print("known customer")
        user_vec = W[user_index[customer_id]]
        scores_personal = pd.Series(user_vec @ H, index=product_index.keys())
        
        # Hybrid case: also clicked product
        if product_id and product_id in sim_df.columns:
            print("product id is known>>>>hybrid")
            scores_context = sim_df[product_id]
            #print("scores_context",scores_context)
            # Normalize (avoid scale mismatch)
            scores_personal = (scores_personal - scores_personal.min()) / (scores_personal.max() - scores_personal.min())
            scores_context = (scores_context - scores_context.min()) / (scores_context.max() - scores_context.min())
            print("scores_context",scores_context.sort_values(ascending=False).head(top_n))
            print("scores_personal",scores_personal.sort_values(ascending=False).head(top_n))
            final_scores = alpha * scores_personal + (1 - alpha) * scores_context
        else:
            print("Product id is unknown")
            final_scores = scores_personal
        print("Top 5 result with Hybrid search>>>>",final_scores.sort_values(ascending=False).head(top_n))
        return final_scores.sort_values(ascending=False).head(top_n)
    
    # Guest browsing
    elif product_id:
        print("guest user")
        return sim_df[product_id].sort_values(ascending=False).iloc[1:top_n+1]
    
    else:
        raise ValueError("Need either customer_id or product_id.")
# print("Known user only:")
# print(recommend(customer_id="3bf8eb03-7f30-4370-9c6a-ad052e3549a3", top_n=3))

# print("\nGuest browsing only:")
# print(recommend(product_id="REF 111TA2234", top_n=3))

#print("\nKnown user clicking a product (hybrid):")
#print(recommend(customer_id="00007219-b164-444f-9d9a-a5d51208317a", product_id="REF 165TA4768", top_n=3))
