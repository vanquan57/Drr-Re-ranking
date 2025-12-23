#! -*- coding: utf-8 -*-
"""
Demo script để visualize kết quả re-ranking
"""
import json
import sys

def load_test_data(test_file, predict_file, num_samples=5):
    """Load test data và predictions"""
    # Load test data
    test_lines = []
    with open(test_file, 'r') as f:
        for i, line in enumerate(f):
            if i >= num_samples:
                break
            test_lines.append(line.strip())
    
    # Load predictions
    predict_lines = []
    with open(predict_file, 'r') as f:
        for i, line in enumerate(f):
            if i >= num_samples:
                break
            predict_lines.append(line.strip())
    
    return test_lines, predict_lines

def parse_test_line(line):
    """Parse 1 dòng test data"""
    parts = line.split('|')
    uid = parts[0]
    ucf = json.loads(parts[1])
    icf = json.loads(parts[2])
    pv = json.loads(parts[3])
    iv = json.loads(parts[4])
    labels = json.loads(parts[5])
    return uid, ucf, icf, pv, iv, labels

def parse_predict_line(line):
    """Parse 1 dòng prediction"""
    parts = line.split('\t')
    original_labels = json.loads(parts[0])
    reranked_labels = json.loads(parts[1])
    return original_labels, reranked_labels

def visualize_reranking(test_line, predict_line, sample_idx):
    """Visualize kết quả re-ranking cho 1 sample"""
    # Parse data
    uid, ucf, icf, pv, iv, labels = parse_test_line(test_line)
    original_labels, reranked_labels = parse_predict_line(predict_line)
    
    print("\n" + "="*80)
    print(f"SAMPLE {sample_idx + 1}")
    print("="*80)
    
    # User info
    print(f"\nUser ID: {uid}")
    print(f"   User Features: {ucf}")
    
    # Count clicks
    num_clicked = int(sum(labels))
    print(f"\nTotal items: 30")
    print(f"   User clicked: {num_clicked} items")
    
    # Find clicked items
    clicked_positions = [i for i, label in enumerate(labels) if label == 1.0]
    print(f"   Clicked positions: {clicked_positions}")
    
    # Show items với labels
    print("\n" + "-"*80)
    print("ALL 30 ITEMS - BEFORE RE-RANKING (Original Order)")
    print("-"*80)
    print(f"{'Pos':<5} {'Item ID':<10} {'Category':<10} {'Label':<10} {'Status'}")
    print("-"*80)
    
    for i in range(len(icf)):
        item_id = icf[i][0]
        category = icf[i][1]
        label = "[CLICKED]" if labels[i] == 1.0 else "[Ignored]"
        status = "[*]" if labels[i] == 1.0 else "   "
        print(f"{i+1:<5} {item_id:<10} {category:<10} {label:<10} {status}")
    
    # Re-ranked results
    print("\n" + "-"*80)
    print("ALL 30 ITEMS - AFTER RE-RANKING (Model's Order)")
    print("-"*80)
    print(f"{'Pos':<5} {'Item ID':<10} {'Category':<10} {'Label':<10} {'Status'}")
    print("-"*80)
    
    # Find new positions of items after reranking
    reranked_indices = []
    for i, new_label in enumerate(reranked_labels):
        # Find original index
        for j, orig_label in enumerate(labels):
            if new_label == orig_label:
                if j not in reranked_indices:
                    reranked_indices.append(j)
                    break
    
    for new_pos, orig_idx in enumerate(reranked_indices):
        item_id = icf[orig_idx][0]
        category = icf[orig_idx][1]
        label = "[CLICKED]" if reranked_labels[new_pos] == 1.0 else "[Ignored]"
        status = "[*]" if reranked_labels[new_pos] == 1.0 else "   "
        moved = ""
        if labels[orig_idx] == 1.0:
            if orig_idx != new_pos:
                if orig_idx > new_pos:
                    moved = f" ^ UP (from pos {orig_idx+1})"
                else:
                    moved = f" v DOWN (from pos {orig_idx+1})"
            else:
                moved = f" = (same pos)"
        print(f"{new_pos+1:<5} {item_id:<10} {category:<10} {label:<10} {status}{moved}")
    
    # Calculate improvement for different K values
    print("\n" + "-"*80)
    print("IMPROVEMENT AT DIFFERENT POSITIONS")
    print("-"*80)
    
    for k in [5, 10, 30]:
        original_clicks = sum(labels[:k])
        reranked_clicks = sum(reranked_labels[:k])
        improvement = reranked_clicks - original_clicks
        
        status = "[+]" if improvement > 0 else "[-]" if improvement < 0 else "[=]"
        print(f"Top {k:2d}: Original={int(original_clicks)}, Re-ranked={int(reranked_clicks)}, "
              f"Change={int(improvement):+d} {status}")
    
    # Overall summary
    total_improvement = sum(reranked_labels[:10]) - sum(labels[:10])
    if total_improvement > 0:
        print(f"\nOverall: Model moved {int(total_improvement)} more relevant items into top 10!")

def main():
    """Main function"""
    test_file = 'dataset/rec_test_set.sample.txt'
    predict_file = 'dataset/rec_test_set.sample.txt.predict.out'
    
    # Get number of samples to show
    num_samples = 5
    if len(sys.argv) > 1:
        num_samples = int(sys.argv[1])
    
    print("="*80)
    print("DRR MODEL - RE-RANKING DEMO")
    print("="*80)
    print(f"\nShowing {num_samples} samples...")
    print("(Run with: python demo_visualization.py <num_samples>)")
    
    # Load data
    test_lines, predict_lines = load_test_data(test_file, predict_file, num_samples)
    
    # Visualize each sample
    for i, (test_line, predict_line) in enumerate(zip(test_lines, predict_lines)):
        visualize_reranking(test_line, predict_line, i)
    
    print("\n" + "="*80)
    print("Demo completed!")
    print("="*80)

if __name__ == "__main__":
    main()

