import numpy as np
from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.utils import get_action_masks
from sapai_gym import SuperAutoPetsEnv
from sapai_gym.opponent_gen.opponent_generators import random_opp_generator
from tqdm import tqdm
from sapai_gym.SuperAutoPetsEnv import get_action_name

NUM_GAMES = 100
MODEL_PATH = "model_sap_gym_sb3_180822_checkpoint_2175_steps"  # Update with your actual model name

def interpret_action(action_id, env):
    """Returns a human-readable string for a given action."""
    all_actions = env._avail_actions()
    if action_id not in all_actions:
        return f"Invalid action {action_id}"

    action_tuple = all_actions[action_id]
    action_name = get_action_name(action_id)

    if action_name == "buy_pet":
        return f"Buy pet from shop slot {action_tuple[1]}"
    elif action_name == "buy_food":
        return f"Buy food from shop slot {action_tuple[1]} for team slot {action_tuple[2]}"
    elif action_name == "buy_food_team":
        return f"Buy food from shop slot {action_tuple[1]} (random team target)"
    elif action_name == "buy_combine":
        return f"Buy pet from shop slot {action_tuple[1]} and combine with team slot {action_tuple[2]}"
    elif action_name == "combine":
        return f"Combine team pets at slot {action_tuple[1]} and {action_tuple[2]}"
    elif action_name == "sell":
        return f"Sell pet at team slot {action_tuple[1]}"
    elif action_name == "roll":
        return f"Roll the shop"
    elif action_name == "end_turn":
        return f"End turn"
    elif action_name == "reorder":
        return f"Reorder team to: {action_tuple[1]}"
    else:
        return f"Unknown action: {action_name} (ID {action_id})"

def simulate_games(model_path, num_games):
    env = SuperAutoPetsEnv(random_opp_generator, valid_actions_only=True)
    model = MaskablePPO.load(model_path)

    win_count = 0
    total_reward = 0
    game_lengths = []

    for game_num in tqdm(range(num_games), desc="Simulating games"):
        obs = env.reset()
        done = False
        reward_sum = 0
        turn = 1
        steps = 0

        print(f"\n=== Starting Game {game_num + 1} ===\n")

        while not done:
            action_masks = env.action_masks()
            action, _ = model.predict(obs, action_masks=action_masks, deterministic=True)

            readable = interpret_action(int(action), env)
            print(f"Turn {env.player.turn}: {readable}")

            obs, reward, done, info = env.step(int(action))
            reward_sum += reward
            steps += 1

            if readable == "End turn":
                result = "Loss"
                if env.player.lf_winner:
                    result = "Victory"
                elif env.player.lives <= 0:
                    result = "Defeat"
                print(f"Turn {env.player.turn - 1}: Battle result: {result}")

        final_result = (
            "Victory (10 wins)"
            if env.player.wins >= 10 else
            "Defeat (0 lives)"
        )
        print(f"\n=== Game {game_num + 1} Finished: {final_result}, Reward: {reward_sum:.2f} ===")
        print(f"Turns played: {env.player.turn}\n")

        if env.player.wins >= 10:
            win_count += 1
        total_reward += reward_sum
        game_lengths.append(env.player.turn)

    avg_reward = total_reward / num_games
    avg_turns = sum(game_lengths) / num_games
    win_rate = win_count / num_games * 100

    print("\n========== Simulation Summary ==========")
    print(f"Total games: {num_games}")
    print(f"Win count: {win_count}")
    print(f"Win rate: {win_rate:.2f}%")
    print(f"Average reward: {avg_reward:.3f}")
    print(f"Average game length (turns): {avg_turns:.2f}")
    print("========================================\n")

if __name__ == "__main__":
    simulate_games(MODEL_PATH, NUM_GAMES)