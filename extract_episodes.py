import logging
from pathlib import Path
from lerobot.common.datasets.lerobot_dataset import LeRobotDataset
import shutil

def extract_episodes(
    source_repo_id: str,
    target_repo_id: str,
    episode_indices: list[int],
    task_description: str = "pick up orange square block and place it cup",
    tags: list[str] = ["so100", "pick_and_place", "clean"],
):
    # Load source dataset
    source_dataset = LeRobotDataset(source_repo_id)
    
    # Create new dataset with same structure
    target_dataset = LeRobotDataset.create(
        target_repo_id,
        fps=source_dataset.fps,
        features=source_dataset.features,
        use_videos=True,
    )
    
    # Copy selected episodes
    for episode_idx in episode_indices:
        logging.info(f"Copying episode {episode_idx}")
        
        # Get episode data
        from_idx = source_dataset.episode_data_index["from"][episode_idx].item()
        to_idx = source_dataset.episode_data_index["to"][episode_idx].item()
        
        # Copy frames
        data = source_dataset.hf_dataset.select(range(from_idx, to_idx))
        for frame_idx in range(len(data)):
            frame = {k: data[k][frame_idx] for k in data.features}
            target_dataset.add_frame(frame)
            
        # Save episode with task description
        target_dataset.save_episode(task_description)
        
    # Copy video files
    logging.info("Copying video files")
    for episode_idx in episode_indices:
        for key in source_dataset.meta.video_keys:
            source_path = source_dataset.meta.get_video_file_path(episode_idx, key)
            target_path = target_dataset.meta.get_video_file_path(target_dataset.num_episodes-1, key)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)
    
    # Consolidate and push to hub
    logging.info("Computing statistics and pushing to hub")
    target_dataset.consolidate(run_compute_stats=True)
    target_dataset.push_to_hub(tags=tags)

if __name__ == "__main__":
    # Configure episodes to keep
    good_episodes = [2, 6, 10, 11, 12, 14, 15, 17, 18, 19, 20, 23, 24, 26, 28, 
                    32, 33, 34, 37, 38, 39, 40, 41, 45, 46, 47, 48, 52, 54, 55]
    
    # Run extraction
    extract_episodes(
        source_repo_id="francescocrivelli/so100_test",
        target_repo_id="francescocrivelli/so100_test_clean",
        episode_indices=good_episodes
    )
