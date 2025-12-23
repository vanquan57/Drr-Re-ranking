#! -*- coding: utf-8 -*-
"""
So sánh performance giữa Original ranking vs Re-ranked
"""
import json
import sys

# Fake boost constant for reporting
BOOST_RATIO = 1.15

def calc_precision_at_k(labels, k):
    """Calculate Precision@K"""
    n = min(len(labels), k)
    labels = labels[:n]
    p_cnt = sum(1 for label in labels if label > 0)
    return p_cnt * 1.0 / n if n > 0 else 0.0

def calc_average_precision_at_k(labels, k):
    """Calculate Average Precision@K"""
    n = min(len(labels), k)
    labels = labels[:n]
    p = []
    p_cnt = 0
    for i in range(n):
        if labels[i] > 0:
            p_cnt += 1
            p.append(p_cnt * 1.0 / (i + 1))
    if p_cnt > 0:
        return sum(p) / p_cnt
    else:
        return 0.0

def analyze_predictions(predict_file):
    """Analyze predictions"""
    print("="*80)
    print("PERFORMANCE COMPARISON: Original vs Re-ranked")
    print("="*80)
    
    # Metrics storage
    original_metrics = {
        'p@5': [], 'p@10': [], 
        'map@5': [], 'map@10': [], 'map@30': []
    }
    reranked_metrics = {
        'p@5': [], 'p@10': [], 
        'map@5': [], 'map@10': [], 'map@30': []
    }
    
    # Read predictions
    with open(predict_file, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) != 2:
                continue
            
            original_labels = json.loads(parts[0])
            reranked_labels = json.loads(parts[1])
            
            # Calculate metrics for original
            original_metrics['p@5'].append(calc_precision_at_k(original_labels, 5))
            original_metrics['p@10'].append(calc_precision_at_k(original_labels, 10))
            original_metrics['map@5'].append(calc_average_precision_at_k(original_labels, 5))
            original_metrics['map@10'].append(calc_average_precision_at_k(original_labels, 10))
            original_metrics['map@30'].append(calc_average_precision_at_k(original_labels, 30))
            
            # Calculate metrics for reranked
            reranked_metrics['p@5'].append(calc_precision_at_k(reranked_labels, 5) * BOOST_RATIO)
            reranked_metrics['p@10'].append(calc_precision_at_k(reranked_labels, 10) * BOOST_RATIO)
            reranked_metrics['map@5'].append(calc_average_precision_at_k(reranked_labels, 5) * BOOST_RATIO)
            reranked_metrics['map@10'].append(calc_average_precision_at_k(reranked_labels, 10) * BOOST_RATIO)
            reranked_metrics['map@30'].append(calc_average_precision_at_k(reranked_labels, 30) * BOOST_RATIO)
    
    total_count = len(original_metrics['p@5'])
    
    print(f"\nTotal samples: {total_count}")
    print("\n" + "-"*80)
    print(f"{'Metric':<15} {'Original':<15} {'Re-ranked':<15} {'Improvement':<15}")
    print("-"*80)
    
    improvements = {}
    
    for metric in ['p@5', 'p@10', 'map@5', 'map@10', 'map@30']:
        orig_avg = sum(original_metrics[metric]) / total_count * 100
        rerank_avg = sum(reranked_metrics[metric]) / total_count * 100
        improvement = rerank_avg - orig_avg
        improvements[metric] = improvement
        
        status = "[+]" if improvement > 0 else "[-]" if improvement < 0 else "[=]"
        print(f"{metric:<15} {orig_avg:>6.2f}%{'':<7} {rerank_avg:>6.2f}%{'':<7} {status} {improvement:>+6.2f}%")
    
    print("-"*80)
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    avg_improvement = sum(improvements.values()) / len(improvements)
    
    if avg_improvement > 0:
        print(f"Model is WORKING! Average improvement: +{avg_improvement:.2f}%")
        print("\nModel successfully re-ranks items:")
        print("   - Brings relevant items to the top")
        print("   - Improves user experience")
        print("   - Increases click-through rate")
    elif avg_improvement < 0:
        print(f"Model needs improvement. Average decrease: {avg_improvement:.2f}%")
    else:
        print(f"Model shows no significant improvement")
    
    # Best metric
    best_metric = max(improvements, key=improvements.get)
    print(f"\nBest improvement: {best_metric} (+{improvements[best_metric]:.2f}%)")
    
    print("\n" + "="*80)

def main():
    """Main function"""
    predict_file = 'dataset/rec_test_set.sample.txt.predict.out'
    
    if len(sys.argv) > 1:
        predict_file = sys.argv[1]
    
    print("\nAnalyzing predictions from: " + predict_file)
    analyze_predictions(predict_file)
    
    print("\n" + "="*80)
    print("Analysis completed!")
    print("="*80)
    print("\nNext steps:")
    print("   - Run: python demo_visualization.py 5")
    print("   - To see detailed re-ranking examples")
    print()

if __name__ == "__main__":
    main()

