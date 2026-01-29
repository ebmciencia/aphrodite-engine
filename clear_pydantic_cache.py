#!/usr/bin/env python3
"""
Script para limpar o cache do Pydantic e forçar a recompilação dos modelos.
Deve ser executado após a instalação do Aphrodite no Docker.
"""
import os
import sys
from pathlib import Path


def clear_pycache(directory: Path):
    """Remove todos os arquivos __pycache__ e .pyc recursivamente."""
    count = 0
    for root, dirs, files in os.walk(directory):
        # Remove __pycache__ directories
        if '__pycache__' in dirs:
            pycache_dir = Path(root) / '__pycache__'
            for pyc_file in pycache_dir.glob('*.pyc'):
                pyc_file.unlink()
                count += 1
            try:
                pycache_dir.rmdir()
            except OSError:
                pass
        
        # Remove standalone .pyc files
        for file in files:
            if file.endswith('.pyc'):
                pyc_path = Path(root) / file
                pyc_path.unlink()
                count += 1
    
    return count


if __name__ == "__main__":
    # Encontra o diretório de instalação do Aphrodite
    try:
        import aphrodite
        aphrodite_path = Path(aphrodite.__file__).parent
        print(f"Limpando cache do Pydantic em: {aphrodite_path}")
        
        count = clear_pycache(aphrodite_path)
        print(f"✅ Removidos {count} arquivos de cache .pyc")
        
        # Também limpa o cache do Pydantic especificamente
        pydantic_cache = aphrodite_path / "config" / "__pycache__"
        if pydantic_cache.exists():
            print(f"Limpando cache específico do Pydantic em: {pydantic_cache}")
            for pyc_file in pydantic_cache.glob('*.pyc'):
                pyc_file.unlink()
                print(f"  - Removido: {pyc_file.name}")
        
        print("✅ Cache limpo com sucesso!")
        sys.exit(0)
    except ImportError:
        print("❌ Erro: Aphrodite não está instalado")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao limpar cache: {e}")
        sys.exit(1)
