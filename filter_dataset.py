from lerobot.common.datasets.lerobot_dataset import LeRobotDataset

# List of good episodes
good_episodes = [2, 6, 10, 11, 12, 14, 15, 17, 18, 19, 20, 23, 24, 26, 28, 
                32, 33, 34, 37, 38, 39, 40, 41, 45, 46, 47, 48, 52, 54, 55]

# Load your original dataset 
original_dataset = LeRobotDataset("francescocrivelli/so100_test")

# Calculate episodes to remove (all episodes not in good_episodes)
all_episodes = list(range(original_dataset.num_episodes))
episodes_to_remove = [ep for ep in all_episodes if ep not in good_episodes]

# Create new dataset ID for the filtered version
filtered_repo_id = "francescocrivelli/so100_test_filtered"

# Create a new dataset with only the good episodes
filtered_dataset = LeRobotDataset.create(
    filtered_repo_id,
    fps=original_dataset.fps,
    features=original_dataset.features,
    use_videos=True
)

# Copy over only the good episodes
for episode_idx in good_episodes:
    # Get data for this episode
    from_idx = original_dataset.episode_data_index["from"][episode_idx]
    to_idx = original_dataset.episode_data_index["to"][episode_idx]
    
    # Copy each frame from original to filtered dataset
    for idx in range(from_idx, to_idx):
        frame = {k: v[idx] for k, v in original_dataset.hf_dataset.items()}
        filtered_dataset.add_frame(frame)
    
    # Save episode with original task description
    task = original_dataset.meta.episodes[episode_idx]["tasks"]
    filtered_dataset.save_episode(task)

# Consolidate the filtered dataset
filtered_dataset.consolidate(run_compute_stats=True)

# Push to hub if desired
filtered_dataset.push_to_hub(tags=["filtered", "good_episodes"])