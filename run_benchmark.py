from ai_trainer import CyberpunkAITrainer

if __name__ == '__main__':
    trainer = CyberpunkAITrainer()
    trainer.start_training_session((10,10),15)
    metrics = trainer.train_batch(200)
    print('\nBATCH METRICS:\n', metrics)
