import polars as pl
import numpy as np
from sklearn.manifold import MDS
from sklearn.metrics import pairwise_distances

def mds_batches(
    df: pl.DataFrame,
    batch_size: int = 1000,
    n_landmarks: int = 1000,
    n_components: int = 2,
    random_state: int = 42
) -> pl.DataFrame:
    """
    Compute MDS in batches using Landmark MDS to preserve global structure.
    
    Parameters:
    - df: Polars DataFrame with features.
    - batch_size: Rows per batch.
    - n_landmarks: Number of landmarks for global structure.
    - n_components: Output dimensions (default=2).
    
    Returns:
    - Polars DataFrame with 2D embeddings.
    """
    # =================================================================
    # Step 1: Select Landmarks (Random Sample)
    # =================================================================
    # If the dataset is larger than n_landmarks, sample landmarks
    if len(df) > n_landmarks:
        landmarks = df.sample(n=n_landmarks, seed=random_state).to_pandas()
    else:
        landmarks = df.to_pandas()
    
    # =================================================================
    # Step 2: Compute MDS on Landmarks (Global Structure)
    # =================================================================
    # Compute distance matrix for landmarks
    D_landmarks = pairwise_distances(landmarks)
    
    # Fit MDS to landmarks
    mds = MDS(
        n_components=n_components,
        dissimilarity='precomputed',
        random_state=random_state
    )
    Y_landmarks = mds.fit_transform(D_landmarks)  # Landmark embeddings
    
    # Precompute terms for projection
    Y_pinv = np.linalg.pinv(Y_landmarks)  # Pseudoinverse of landmarks
    D_landmarks_sq = D_landmarks ** 2
    mu = D_landmarks_sq.mean(axis=0)  # Mean squared distances
    
    # =================================================================
    # Step 3: Project All Data in Batches Using Landmarks
    # =================================================================
    results = []
    for i in range(0, len(df), batch_size):
        batch = df.slice(i, batch_size).to_pandas()
        
        # Compute squared distances from batch to landmarks
        D_batch_to_landmarks_sq = pairwise_distances(batch, landmarks) ** 2
        
        # Project into landmark space (LMDS formula)
        projected = -0.5 * (D_batch_to_landmarks_sq - mu) @ Y_pinv.T
        
        # Store results
        results.append(
            pl.DataFrame(projected, schema=[f"dim_{j}" for j in range(n_components)])
        )

    return pl.concat(results)


def mds_classic(
    df: pl.DataFrame,
    n_components: int = 2,
    metric: bool = True
) -> pl.DataFrame:
    """
    Compute MDS embedding (Classical MDS for metric=True, SMACOF for metric=False).
    
    Parameters:
    - df: Polars DataFrame with features (n_samples x n_features)
    - n_components: Dimension of the embedded space
    - metric: If True, use Classical MDS (exact). If False, use SMACOF (iterative).
    
    Returns:
    - Polars DataFrame with MDS coordinates (n_samples x n_components)
    """
    X = df.to_numpy()
    D = pairwise_distances(X)  # Pairwise distance matrix
    
    if metric:
        # Classical MDS (Eigendecomposition)
        n = D.shape[0]
        H = np.eye(n) - np.ones((n, n)) / n  # Centering matrix
        B = -0.5 * H @ (D ** 2) @ H  # Double-centering
        
        # Eigen decomposition
        eigvals, eigvecs = np.linalg.eigh(B)
        idx = np.argsort(eigvals)[::-1][:n_components]
        components = eigvecs[:, idx] @ np.diag(np.sqrt(eigvals[idx]))
    else:
        # SMACOF (Scikit-learn's implementation)
        from sklearn.manifold import MDS
        components = MDS(
            n_components=n_components,
            dissimilarity='precomputed',
            random_state=0
        ).fit_transform(D)
    
    return pl.DataFrame(
        components,
        schema=[f"MDS_{i+1}" for i in range(n_components)]
    )