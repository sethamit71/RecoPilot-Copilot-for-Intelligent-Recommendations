import pandas as pd
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from config.settings import CUSTOMER_BOUGHT_FILE,NMF_W,NMF_H,NMF_USER_INDEX,NMF_PRODUCT_INDEX,NMF_SIM_DF
# ----------------------
# 1. Load your data
# Sample dataframe
df = pd.read_csv(CUSTOMER_BOUGHT_FILE)
# ----------------------

# Expand purchases
df_expanded = (
    df.set_index("CustomerID")["PurchasedArticles"]
      .str.split(",", expand=True)
      .stack()
      .reset_index(level=1, drop=True)
      .reset_index()
)
df_expanded.columns = ["CustomerID", "ProductID"]

# User-Item Matrix
user_item = pd.crosstab(df_expanded["CustomerID"], df_expanded["ProductID"])


# 2. Train NMF

nmf = NMF(n_components=5, init="nndsvda", random_state=42)
W = nmf.fit_transform(user_item)   # Customers × factors
H = nmf.components_                # Factors × Products

# 3. Save artifacts
joblib.dump(W, NMF_W)
joblib.dump(H, NMF_H)
joblib.dump({uid: idx for idx, uid in enumerate(user_item.index)}, NMF_USER_INDEX)
joblib.dump({pid: idx for idx, pid in enumerate(user_item.columns)}, NMF_PRODUCT_INDEX)

# Product embeddings
product_embeddings = H.T
product_embeddings = pd.DataFrame(product_embeddings, index=user_item.columns)

# Precompute similarity for guest mode
from sklearn.metrics.pairwise import cosine_similarity
sim_matrix = cosine_similarity(product_embeddings)
sim_df = pd.DataFrame(sim_matrix, index=user_item.columns, columns=user_item.columns)
sim_df.to_pickle(NMF_SIM_DF)

print(">>>>>>Training complete. Artifacts saved.")
