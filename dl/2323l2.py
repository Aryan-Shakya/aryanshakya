# LAB 2: Unsupervised Learning - K-Means Clustering and PCA

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, adjusted_rand_score

sns.set(style="whitegrid")

print("Lab 2 - Unsupervised Learning: K-Means Clustering and PCA")

iris = load_iris()
X = iris.data
df = pd.DataFrame(X, columns=iris.feature_names)
df["species"] = pd.Categorical.from_codes(iris.target, iris.target_names)

print("Dataset Shape:", df.shape)
print(df.head())

sns.pairplot(df, hue="species", corner=True)
plt.show()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Mean after scaling:", X_scaled.mean(axis=0).round(2))
print("Std  after scaling:", X_scaled.std(axis=0).round(2))

inertias, silhouettes = [], []
k_values = range(2, 11)

for k in k_values:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    silhouettes.append(silhouette_score(X_scaled, labels))

plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.plot(k_values, inertias, marker="o", color="blue")
plt.title("Elbow Method", fontsize=14)
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")

plt.subplot(1,2,2)
plt.plot(k_values, silhouettes, marker="o", color="green")
plt.title("Silhouette Score", fontsize=14)
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Score")

plt.tight_layout()
plt.show()

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)
df["cluster"] = clusters

print("Cluster assignments:\n", clusters)
print("\nSilhouette Score:", round(silhouette_score(X_scaled, clusters), 3))
print("Adjusted Rand Index (vs true species):", round(adjusted_rand_score(iris.target, clusters), 3))

centres = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=iris.feature_names)
print("\nCluster Centres (original units):\n")
print(centres.round(2))

print("\nCluster vs Species:\n")
print(pd.crosstab(df["cluster"], df["species"]))

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print("Explained Variance Ratio:", pca.explained_variance_ratio_.round(4))
print("Total Variance Explained:", round(pca.explained_variance_ratio_.sum() * 100, 2), "%")

loadings = pd.DataFrame(pca.components_.T, columns=["PC1", "PC2"], index=iris.feature_names)
print("\nPCA Loadings:\n")
print(loadings.round(3))

centroids_pca = pca.transform(kmeans.cluster_centers_)

plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.scatter(X_pca[:,0], X_pca[:,1], c=clusters, cmap="viridis", s=50)
plt.scatter(centroids_pca[:,0], centroids_pca[:,1], c="red", marker="X", s=250, label="Centroids")
plt.title("K-Means Clustering using PCA", fontsize=14)
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend()

plt.subplot(1,2,2)
plt.scatter(X_pca[:,0], X_pca[:,1], c=iris.target, cmap="viridis", s=50)
plt.title("Actual Species", fontsize=14)
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")

plt.tight_layout()
plt.show()

pca_full = PCA().fit(X_scaled)
cumulative = np.cumsum(pca_full.explained_variance_ratio_)

plt.figure(figsize=(8,5))
plt.bar(range(1,5), pca_full.explained_variance_ratio_, alpha=0.6, label="Individual")
plt.step(range(1,5), cumulative, where="mid", color="red", label="Cumulative")
plt.xticks(range(1,5))
plt.xlabel("Principal Component")
plt.ylabel("Explained Variance Ratio")
plt.title("Scree Plot", fontsize=14)
plt.legend()
plt.show()

pca3 = PCA(n_components=3)
X_pca3 = pca3.fit_transform(X_scaled)

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection="3d")
scatter = ax.scatter(X_pca3[:,0], X_pca3[:,1], X_pca3[:,2], c=clusters, cmap="viridis", s=50)

ax.set_title("3D Visualization of K-Means Clusters", fontsize=14)
ax.set_xlabel("PCA 1")
ax.set_ylabel("PCA 2")
ax.set_zlabel("PCA 3")

legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
ax.add_artist(legend1)
plt.show()

# Algorithm
# 1. Import the libraries and load the Iris dataset; keep the species only for later comparison.
# 2. Draw a pair plot to understand the relationship between features.
# 3. Standardise the features with StandardScaler.
# 4. Run K-Means for k = 2 to 10 and plot the Elbow curve (inertia) and Silhouette score.
# 5. Apply K-Means with k = 3, print cluster centres and cross-tabulate clusters against species.
# 6. Apply PCA with two components, print explained variance and component loadings.
# 7. Plot the clusters and centroids in PCA space beside the actual species.
# 8. Plot a scree plot and a 3D PCA visualisation of the clusters.
