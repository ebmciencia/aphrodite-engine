#!/usr/bin/env python3
"""
Script para verificar a configuração do AphroditeConfig dentro do container.
"""
import sys
from pathlib import Path

try:
    import aphrodite
    from aphrodite.config import AphroditeConfig
    
    # Encontra o arquivo aphrodite.py
    config_file = Path(aphrodite.__file__).parent / "config" / "aphrodite.py"
    
    print(f"📍 Arquivo de configuração: {config_file}")
    print(f"📦 Versão do Aphrodite: {aphrodite.__version__}")
    
    # Lê as primeiras 100 linhas do arquivo
    with open(config_file, 'r') as f:
        lines = f.readlines()
    
    print("\n🔍 Verificando linhas 55-90 do arquivo:")
    print("=" * 70)
    for i, line in enumerate(lines[54:90], start=55):
        print(f"{i:3d}| {line.rstrip()}")
    print("=" * 70)
    
    # Verifica a configuração do dataclass
    import dataclasses
    from pydantic.dataclasses import is_pydantic_dataclass
    
    print(f"\n✅ AphroditeConfig é Pydantic dataclass: {is_pydantic_dataclass(AphroditeConfig)}")
    
    # Tenta ver a configuração do Pydantic
    if hasattr(AphroditeConfig, '__pydantic_config__'):
        config = AphroditeConfig.__pydantic_config__
        print(f"⚙️  Configuração Pydantic:")
        print(f"   - extra: {getattr(config, 'extra', 'NÃO DEFINIDO')}")
        print(f"   - arbitrary_types_allowed: {getattr(config, 'arbitrary_types_allowed', 'NÃO DEFINIDO')}")
    
    # Tenta criar uma instância de teste
    print("\n🧪 Testando criação de instância...")
    try:
        from aphrodite.config import (
            ModelConfig, CacheConfig, ParallelConfig, 
            SchedulerConfig, DeviceConfig, LoadConfig
        )
        
        config = AphroditeConfig(
            scale_dtype=None,
            zp_dtype=None,
        )
        print("✅ SUCESSO: Instância criada com scale_dtype e zp_dtype!")
    except Exception as e:
        print(f"❌ ERRO ao criar instância: {e}")
        import traceback
        traceback.print_exc()
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
