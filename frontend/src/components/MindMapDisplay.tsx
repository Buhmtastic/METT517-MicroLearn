import React, { useEffect, useRef } from 'react';
import mermaid from 'mermaid';

// 마인드맵 데이터 노드의 타입 정의
interface MindMapNode {
  name: string;
  children?: MindMapNode[];
}

interface Props {
  mindmapData: MindMapNode;
}

// JSON 데이터를 Mermaid 구문으로 변환하는 재귀 함수
const jsonToMermaidSyntax = (node: MindMapNode, parentId: string, idCounter: { val: number }): string => {
  let syntax = '';
  if (!node || !node.name) return '';

  idCounter.val++;
  const currentNodeId = `node${idCounter.val}`;
  // Mermaid는 노드 ID에 특수문자를 허용하지 않으므로 간단한 ID를 사용합니다.
  // 실제 텍스트는 노드 레이블에 표시합니다.
  syntax += `    ${parentId} --> ${currentNodeId}["${node.name.replace(/"/g, '&quot;')}"]\n`;

  if (node.children && node.children.length > 0) {
    node.children.forEach(child => {
      syntax += jsonToMermaidSyntax(child, currentNodeId, idCounter);
    });
  }
  return syntax;
};

const MindMapDisplay: React.FC<Props> = ({ mindmapData }) => {
  const mermaidRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const renderMermaid = async () => {
      if (mermaidRef.current && mindmapData) {
        try {
          // Mermaid 구문 생성
          let mermaidSyntax = 'graph TD\n';
          const idCounter = { val: 0 };
          const rootId = `node${idCounter.val}`;
          mermaidSyntax += `    ${rootId}["${mindmapData.name.replace(/"/g, '&quot;')}"]\n`;
          
          if (mindmapData.children) {
            mindmapData.children.forEach(child => {
              mermaidSyntax += jsonToMermaidSyntax(child, rootId, idCounter);
            });
          }

          // Mermaid 렌더링 (Promise-based API)
          const { svg } = await mermaid.render('mermaid-graph', mermaidSyntax);
          if (mermaidRef.current) {
            mermaidRef.current.innerHTML = svg;
          }
        } catch (e) {
          console.error("Error rendering Mermaid chart:", e);
          if (mermaidRef.current) {
            mermaidRef.current.innerHTML = '마인드맵을 렌더링하는 중 오류가 발생했습니다.';
          }
        }
      }
    };
    renderMermaid();
  }, [mindmapData]);

  return <div ref={mermaidRef} className="mermaid-container"></div>;
};

export default MindMapDisplay;